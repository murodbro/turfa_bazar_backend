from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from store.models import Product, ProductVariation
from user.models import Account

from .serializers import CartItemSerializer
from .models import CartItem


class CartItemApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_user(self, user_id):
        user = Account.objects.filter(id=user_id).first()
        if not user:
            return Response({"ok": False, "message": "Foydalanuvchi topilmadi"})
        return user

    def get_product(self, product_id):
        product = Product.objects.filter(id=product_id).first()
        if not product:
            return Response({"ok": False, "message": "Mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        return product

    def get(self, request, user_id):
        user = self.get_user(user_id)
        cart_items = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(serializer.data)

    def post(self, request, user_id):
        product_id = request.data.get("productId")
        variation_id = request.data.get("variationId")
        user = self.get_user(user_id)
        product = self.get_product(product_id)

        variation = ProductVariation.objects.filter(id=variation_id).first()
        cart_item = CartItem.objects.filter(user=user, product=product, product_variation=variation).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(user=user, product=product, product_variation=variation, quantity=1)

        return Response({"ok": True, "message": "Savatga yangi mahsulot qo'shildi"}, status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        variation_id = request.data.get("variationId")
        action = request.data.get("action")
        user = self.get_user(user_id)

        variation = ProductVariation.objects.filter(id=variation_id).first()
        cart_item = CartItem.objects.filter(user=user, product_variation=variation).first()

        if not cart_item:
            return Response(
                {"ok": False, "message": "Savatingizdagi mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        if action == "remove":
            if cart_item.quantity == 1:
                cart_item.delete()
                return Response(
                    {"ok": True, "message": "Savatingizdagi mahsulot savatdan o'chirildi"}, status=status.HTTP_200_OK
                )
            else:
                cart_item.quantity -= 1
                cart_item.save()
                return Response(
                    {"ok": True, "message": "Savatingizdagi mahsulot bittaga kamaydi"}, status=status.HTTP_200_OK
                )

        if action == "adding":
            cart_item.quantity += 1
            cart_item.save()
            return Response(
                {"ok": True, "message": "Savatingizdagi mahsulot bittaga ortdi"}, status=status.HTTP_200_OK
            )

        return Response({"ok": False, "message": "Noto'g'ri amal"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        variation_id = request.data.get("variationId")
        user = self.get_user(user_id)

        variation = ProductVariation.objects.filter(id=variation_id).first()
        cart_item = CartItem.objects.filter(user=user, product_variation=variation).first()

        if not cart_item:
            return Response(
                {"ok": False, "message": "Savatingizdagi mahsulot topilmadi"}, status=status.HTTP_404_NOT_FOUND
            )

        cart_item.delete()

        return Response(
            {"ok": True, "message": "Savatingizdagi mahsulot savatdan o'chirildi"}, status=status.HTTP_200_OK
        )
