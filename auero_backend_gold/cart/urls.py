from django.urls import path
from .views import (
    UserCartView, UserCartAddView, UserCartRemoveView, UserCartUpdateView, UserCartClearView,
    GuestCartView, GuestCartAddView, GuestCartRemoveView, GuestCartUpdateView, GuestCartClearView,
    CartMergeView
)

urlpatterns = [
    # User cart endpoints
    path('user/', UserCartView.as_view(), name='user-cart'),
    path('user/add/', UserCartAddView.as_view(), name='user-cart-add'),
    path('user/remove/', UserCartRemoveView.as_view(), name='user-cart-remove'),
    path('user/update/', UserCartUpdateView.as_view(), name='user-cart-update'),
    path('user/clear/', UserCartClearView.as_view(), name='user-cart-clear'),

    # Guest cart endpoints
    path('guest/', GuestCartView.as_view(), name='guest-cart'),
    path('guest/add/', GuestCartAddView.as_view(), name='guest-cart-add'),
    path('guest/remove/', GuestCartRemoveView.as_view(), name='guest-cart-remove'),
    path('guest/update/', GuestCartUpdateView.as_view(), name='guest-cart-update'),
    path('guest/clear/', GuestCartClearView.as_view(), name='guest-cart-clear'),

    # Merge guest cart into user cart
    path('merge/', CartMergeView.as_view(), name='cart-merge'),
] 