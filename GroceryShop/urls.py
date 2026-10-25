from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from posApp import views


urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'products/',
        views.products,
        name='products'
    ),

    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'delete-product/<int:id>/',
        views.delete_product,
        name='delete_product'
    ),

    # CART

    path(
        'add-to-cart/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'remove-from-cart/<int:id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    # CHECKOUT

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)