import xendit
from xendit.apis import InvoiceApi
from django.conf import settings
from xendit.invoice.model.create_invoice_request import CreateInvoiceRequest

xendit.set_api_key(settings.XENDIT_API_KEY)
api_client = xendit.ApiClient()
invoice_instance = InvoiceApi(api_client)
create_invoice_request = CreateInvoiceRequest(
    external_id="invoice-20250628-001",
    amount=100000.0,  # In IDR
    description="Checkout for Product ABC",
    payer_email="customer@example.com",
    customer={
        "given_names": "Hadziq",
        "email": "customer@example.com",
    },
    success_redirect_url="https://yourdomain.com/payment/success",
) # CreateInvoiceRequest
