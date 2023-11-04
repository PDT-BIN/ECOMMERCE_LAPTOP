from django.urls import path

from . import views


app_name = 'orders'
urlpatterns = [
    # ORDER.
    path('<int:choice>', views.order_page, name="order-page"),
    path('cancel-order/<int:pk>', views.cancel_order, name='cancel-order'),
    # PRODUCT DETAIL.
    path('buy-now/', views.buy_now, name='buy-now'),
    path('product/<int:pk>', views.product_detail, name='product'),
    path('purchase-cart/<int:pk>', views.purchase_cart, name='purchase-cart'),
    # CART.
    path('cart/', views.cart_page, name='cart-page'),
    path('create-cart/<int:pk>', views.create_cart, name='create-cart'),
    path('update-cart/<int:pk>', views.update_cart, name='update-cart'),
    path('delete-cart/<int:pk>', views.delete_cart, name='delete-cart'),
    path('create-order/', views.create_order, name="create-order")
]
