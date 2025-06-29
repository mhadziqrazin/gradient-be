import time
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import MOCK_PRODUCT
from django.conf import settings

class ProductView(APIView):
    def get(self, request):
        return Response(MOCK_PRODUCT)

class CreatePaymentView(APIView):
    def post(self, request):
        try:
            product_id = request.data.get("product_id")
            channel_code = request.data.get("channel_code")

            if product_id is None or channel_code is None:
                return Response({ "error": "product_id and channel_code are required" }, status=status.HTTP_400_BAD_REQUEST)

            product = MOCK_PRODUCT[product_id]
            product_discount_amount = product["price"] * product["discount"]
            product_final_price = product["price"] - product_discount_amount

            payload = {
                "reference_id": f"test-{int(time.time() * 1000)}", # time miliseconds
                "type": "PAY",
                "country": "ID",
                "currency": "IDR",
                "request_amount": product_final_price,
                "metadata": {
                    "product_name": product["name"],
                    "product_price": product["price"],
                    "product_discount": product["discount"],
                    "product_final_price": product_final_price,
                },
                "channel_code": channel_code,
            }

            response = requests.post(
                "https://api.xendit.co/v3/payment_requests",
                headers={
                    "Content-Type": "application/json",
                    "api-version": "2024-11-11",
                },
                auth=(settings.XENDIT_API_KEY, ""),
                json=payload
            )

            if response.status_code == 201:
                return Response(response.json(), status=status.HTTP_201_CREATED)

            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)