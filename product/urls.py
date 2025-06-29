from django.urls import path
from .views import ProductView, CreatePaymentView
# from .views import ProductView, PurchaseProductView

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('pay/', CreatePaymentView.as_view(), name='payment'),
    # path('purchase/', PurchaseProductView.as_view(), name='product'),
]
