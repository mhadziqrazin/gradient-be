from django.urls import path
from .views import ProductView, PaymentView

urlpatterns = [
    path('', ProductView.as_view(), name='product-list'),
    path('<int:id>/', ProductView.as_view(), name='product-by-id'),
    path('pay/', PaymentView.as_view(), name='payment'),
    path('pay/verify/<str:id>/', PaymentView.as_view(), name='get-payment-by-id'),
]
