# urls.py

from django.urls import path
from .views import (
    VendorListCreateView,
    VendorDetailView,
    PurchaseOrderListCreateView,
    PurchaseOrderDetailView,
    VendorPerformanceView,
    AcknowledgePurchaseOrderView,
)

urlpatterns = [
    # Vendor URLs
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),

    # Purchase Order URLs
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderDetailView.as_view(), name='purchase-order-detail'),

    # Vendor Performance URL
    path('api/vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),

    # Acknowledge Purchase Order URL
    path('api/purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
]
