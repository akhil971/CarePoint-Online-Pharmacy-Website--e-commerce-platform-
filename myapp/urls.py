

from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('shop/',views.shop, name='shop'),
    path('doctor/',views.doctor, name='doctor'),
    path('prescription/',views.prescription, name='prescription'),
    path('contact/',views.contact, name='contact'),
    path('painfever/',views.painfever, name='painfever'),
    path('vitamins/',views.vitamins, name='vitamins'),
    path('coldcough/',views.coldcough, name='coldcough'),
    path('diabetes/',views.diabetes, name='diabetes'),
    path('firstaid/',views.firstaid, name='firstaid'),
    path('skincare/',views.skincare, name='skincare'),
    path('babycare/',views.babycare, name='babycare'),
    path('devices/',views.devices, name='devices'),
    path('doctorappoint/',views.doctorappoint, name='doctorappoint'),
    path('login/',views.login, name='login'),
    path('register/',views.register, name='register'),
    path('logout/', views.logout_view, name='logout'), 

    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]

