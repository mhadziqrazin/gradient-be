import time
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .mock_data import MOCK_PRODUCT
from django.conf import settings

class ProductView(APIView):
    def get(self, request, id=None):
        if id:
            product = next((p for p in MOCK_PRODUCT if p["id"] == id), None)
            if product:
                return Response(product)
            return Response({ "error": f"Product with id {id} not found" }, status=status.HTTP_400_BAD_REQUEST)

        return Response(MOCK_PRODUCT)

class PaymentView(APIView):
    def get(self, request, id=None):
        if id is None:
            return Response({ "error": "id is required" }, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(
            f"https://api.xendit.co/v2/invoices/{id}",
            headers={ "Content-Type": "application/json" },
            auth=(settings.XENDIT_API_KEY, ""),
        )
        if response.status_code == 200:
            data = response.json()
            payment_status = data["status"]

            if payment_status != "PAID":
                return Response({ "error": "Product hasn't been purchased" }, status=status.HTTP_402_PAYMENT_REQUIRED)

            return Response({ "message": "Success" }, status=status.HTTP_200_OK)

        return Response(response.json(), status=response.status_code)

    def post(self, request):
        product_id = request.data.get("product_id")

        if product_id is None:
            return Response({ "error": "product_id is required" }, status=status.HTTP_400_BAD_REQUEST)

        product = next((p for p in MOCK_PRODUCT if p["id"] == product_id), None)
        if product is None:
            return Response({ "error": f"Product with id {id} not found" }, status=status.HTTP_400_BAD_REQUEST)

        product_name = product["name"]
        product_price = product["price"]
        product_discount = product["discount"]
        product_discount_amount = product_price * product_discount
        product_final_price = product_price - product_discount_amount

        payload = {
            "external_id": f"test-{int(time.time() * 1000)}", # 1000 for miliseconds,
            "amount": product_price,
            "description": f"Pembayaran {product_name}",
            "invoice_duration": 10800, # 3 hours
            "customer": {
                "given_names": "John",
                "surname": "Doe",
                "email": "johndoe@example.com",
                "mobile_number": "+6287774441111"
            },
            "success_redirect_url": "http://localhost:3000",
            "failure_redirect_url": "https://www.google.com",
            "currency": "IDR",
            "item": product,
            "metadata": {
                "product_name": product_name,
                "product_price": product_price,
                "product_discount": product_discount,
                "product_final_price": product_final_price,
            },
        }

        try:
            response = requests.post(
                "https://api.xendit.co/v2/invoices",
                headers={ "Content-Type": "application/json" },
                auth=(settings.XENDIT_API_KEY, ""),
                json=payload,
            )

            if response.status_code == 200:
                data = response.json()
                body = {
                    "id": data["id"],
                    "invoice_url": data["invoice_url"],
                }
                return Response(body, status=status.HTTP_200_OK)

            return Response(response.json(), status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)