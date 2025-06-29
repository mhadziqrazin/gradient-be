from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
import uuid

MOCK_DATA = [
    { 'id': 1, 'price': 100, 'name': 'Produk 1' },
    { 'id': 2, 'price': 200, 'name': 'Produk 2' },
    { 'id': 3, 'price': 300, 'name': 'Produk 3' },
]

class ProductView(APIView):
    def get(self, request):
        return Response(ProductSerializer(MOCK_DATA, many=True).data)

class CreateVirtualAccountView(APIView):
    def post(self, request):
        external_id = request.data.get("external_id")
        bank_code = request.data.get("bank_code")
        name = request.data.get("name")

        try:
            return Response({ "message": "Success" }, status=status.HTTP_201_CREATED)
        except xendit.XenditSdkException as e:
            print("Exception when calling PaymentMethodApi->get_balance: %s\n" % e)
