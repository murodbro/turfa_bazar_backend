from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ProductSerializers, ProductDetailSerializers, ReviewSerializer
from .models import Product, ProductReview
from user.models import Account


class ProductListApiView(generics.ListAPIView):
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(is_available=True)


class ProductDetailApiView(generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializers
    queryset = Product.objects.all()
    lookup_field = 'id'


class ProductReviewApiView(APIView):

    def get(self, request, id):
        reviews = ProductReview.objects.filter(product=id).order_by("-created_at")
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, id):
        product = Product.objects.get(id=id)
        user_id = request.data.get("user")
        user = Account.objects.filter(id=user_id).first()

        review = ProductReview.objects.create(
            product=product,
            user=user,
            review=request.data.get("review"),
            image=request.data.get("image")
        )

        # Save the review
        review.save()

        return Response({"ok": True}, status=status.HTTP_201_CREATED)



