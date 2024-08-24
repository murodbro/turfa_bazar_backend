import string
import stripe
import random
from django.db import transaction
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from cart.models import CartItem
from .serializers import OrderSerializer, OrdersHistorySerializers
from .models import Order, OrderItems


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_session(order, user_id, additional_amount=0):
    line_items = []
    total_amount = 0  # Initialize total amount

    for item in order.order_items.all():
        item_amount = int(item.unit_price * 100)
        total_amount += item_amount * item.quantity

        line_items.append(
            {
                "price_data": {
                    "currency": "uzs",
                    "product_data": {
                        "name": item.product.name,
                    },
                    "unit_amount": item_amount,
                },
                "quantity": item.quantity,
            }
        )

    if additional_amount > 0:
        additional_amount_cents = int(additional_amount * 100)
        total_amount += additional_amount_cents

        line_items.append(
            {
                "price_data": {
                    "currency": "uzs",
                    "product_data": {
                        "name": "Kuryer xizmati",
                    },
                    "unit_amount": additional_amount_cents,
                },
                "quantity": 1,
            }
        )

    if total_amount > 99999999:
        raise ValueError("The total amount exceeds the maximum allowed by Stripe.")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=f"{settings.FRONTEND_URL}/order_detail/{order.id}",
        cancel_url=f"{settings.FRONTEND_URL}/cart_items/{user_id}",
    )
    return session


def generate_unique_code():
    while True:
        random_letters = "".join(random.choices(string.ascii_uppercase, k=2))
        random_number = str(random.randint(10000000, 99999999))
        random_code = random_letters + random_number
        if not Order.objects.filter(order_code=random_code).exists():
            return random_code


def generate_smtp():
    return random.randint(100000, 999999)


def send_confirmation_email(smtp_code, email):
    subject = "Tasdiqlash kodi yuborildi!"
    message = f"Sizning emailingiz orqali harid amalga oshirilmoqda. Tasdiqlash kodi [{smtp_code}]. Iltimos buyurtmangizni amalga oshirish uchun ushbu koddan foydalaning.\nAgar ushbu xabar sizga tegishli bo'lmasa shunchaki e'tiborsiz qoldiring."
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


class OrderApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        order_data = request.data
        cart_items = CartItem.objects.filter(user=user_id)
        if not cart_items:
            return Response({"error": "No cart items found for the user."}, status=status.HTTP_400_BAD_REQUEST)

        email = order_data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        order_code = generate_unique_code()
        smtp_code = generate_smtp()

        order_data.update({"user": user_id, "order_code": order_code, "smtp_code": smtp_code})

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            order = serializer.save()

            for cart_item in cart_items:
                OrderItems.objects.create(
                    order=order,
                    product=cart_item.product_variation.product,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product_variation.price,
                    product_variation=cart_item.product_variation,
                )

            try:
                send_confirmation_email(smtp_code, email)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmSMTPApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user_id = request.user.id
        code = request.data.get("smtp_code")
        order_id = request.data.get("order_id")

        if not code:
            return Response({"error": "SMTP code is required."}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id)
        latest_order_with_code = Order.objects.filter(smtp_code=code).latest("created_at")

        if not latest_order_with_code:
            return Response({"error": "Invalid SMTP code."}, status=status.HTTP_400_BAD_REQUEST)

        if order.buy_cash:
            with transaction.atomic():
                order_items = order.order_items.all()
                for item in order_items:
                    if item.status == OrderItems.Status_delivary.PENDING:
                        item.status = OrderItems.Status_delivary.SHIPPED
                        item.confirmed = True
                        item.save()

                cart_items = CartItem.objects.filter(user=user_id)
                for cart_item in cart_items:
                    product_variation = cart_item.product_variation
                    if not product_variation:
                        return Response(
                            {"error": f"Product variation not found for cart item {cart_item.id}."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    product_variation.stock -= cart_item.quantity
                    product_variation.save()
                    cart_item.product.ordered_count += cart_item.quantity
                    cart_item.product.save()
                cart_items.delete()
            return Response({"Ok": True}, status=status.HTTP_201_CREATED)

        else:
            additional_amount = 30000 if order.recive_by_deliver else 0

            try:
                session = create_stripe_session(order, user_id, additional_amount)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            with transaction.atomic():
                order_items = order.order_items.all()
                for item in order_items:
                    if item.status == OrderItems.Status_delivary.PENDING:
                        item.status = OrderItems.Status_delivary.SHIPPED
                        item.confirmed = True
                        item.save()

                cart_items = CartItem.objects.filter(user=user_id)
                for cart_item in cart_items:
                    product_variation = cart_item.product_variation
                    if not product_variation:
                        return Response(
                            {"error": f"Product variation not found for cart item {cart_item.id}."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    product_variation.stock -= cart_item.quantity
                    product_variation.save()
                    cart_item.product.ordered_count += cart_item.quantity
                    cart_item.product.save()
                cart_items.delete()

                return Response({"message": session.url}, status=status.HTTP_201_CREATED)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, order_id):
        order = Order.objects.filter(id=order_id).first()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrdersHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        serializer = OrdersHistorySerializers(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelOrderApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.order_items.all()

        for item in order_items:
            if not item.confirmed:
                item.status = OrderItems.Status_delivary.CANCELED
                item.save()

        return Response({"ok": True}, status=status.HTTP_200_OK)


class CancelOrderStatusApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_items = order.order_items.all()

        for item in order_items:
            if not item.confirmed:
                item.status = OrderItems.Status_delivary.DELIVERED
                item.save()

        return Response({"ok": True}, status=status.HTTP_200_OK)
