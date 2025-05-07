from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomerSignupView,
    VendorSignupView,
    LoginView,
    AddressListCreateView,
    AddressDetailView,
    VendorSignupView,
    LogoutView,
    CurrentUserView
)

urlpatterns = [
    path('signup/customer/', CustomerSignupView.as_view(), name='customer-signup'),
    path('signup/vendor/', VendorSignupView.as_view(), name='vendor-signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('addresses/', AddressListCreateView.as_view(), name='address-list-create'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('vendor-user/', VendorSignupView.as_view(), name='vendor-user'),
]
