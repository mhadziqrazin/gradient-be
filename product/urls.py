from django.urls import path
from .views import ProductView, CreateVirtualAccountView
# from .views import ProductView, PurchaseProductView

urlpatterns = [
    path('', ProductView.as_view(), name='product'),
    path('va/', CreateVirtualAccountView.as_view(), name='virtual_account'),
    # path('purchase/', PurchaseProductView.as_view(), name='product'),
]
