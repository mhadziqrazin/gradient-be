from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .xendit_client import invoice_instance, create_invoice_request
import xendit
import uuid
from pprint import pprint

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
            for_user_id = "62efe4c33e45694d63f585f0"
            response = invoice_instance.create_invoice(create_invoice_request)
            pprint(response)
            # print(response)
            # va = xendit_client.VirtualAccount.create_fixed_va({
            #     "external_id": external_id,
            #     "bank_code": bank_code,
            #     "name": name,
            # })

            # return Response(va, status=status.HTTP_201_CREATED)
            return Response({ "message": "Success" }, status=status.HTTP_201_CREATED)
        except xendit.XenditSdkException as e:
            print("Exception when calling PaymentMethodApi->get_balance: %s\n" % e)

# class PurchaseProductView(APIView):
#     def post(self, request):
#         try:
#             product_id = int(request.data.get('product_id'))
#         except (TypeError, ValueError):
#             return Response({'error': 'Invalid or missing product_id'}, status=status.HTTP_400_BAD_REQUEST)

#         if not 1 <= product_id <= len(MOCK_DATA):
#             return Response({'error': f'product_id must be between 1 and {len(MOCK_DATA)}'}, status=status.HTTP_400_BAD_REQUEST)

#         external_id = f'invoice-{product_id}-{uuid.uuid4().hex}'
#         product = MOCK_DATA[product_id - 1]
#         product_price = product['price']
#         product_name = product['name']

#         # invoice = client.Invoice.create(
#         #     external_id=external_id,
#         #     price=product_price,
#         #     description=f'Payment for order {product_name}',
#         # )

#         return Response(invoice)