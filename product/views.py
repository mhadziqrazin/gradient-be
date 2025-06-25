from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer

class ProductView(APIView):
    def get(self, request):
        MOCK_DATA = [
            { 'price': 100, 'name': 'Produk 1' },
            { 'price': 200, 'name': 'Produk 2' },
            { 'price': 300, 'name': 'Produk 3' },
        ]
        return Response(ProductSerializer(MOCK_DATA, many=True).data)