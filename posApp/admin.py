from django.contrib import admin

from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'quantity'
    )

    search_fields = (
        'name',
        'category'
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'customer_name',
        'phone',
        'total_amount',
        'created_at'
    )

    search_fields = (
        'customer_name',
        'phone'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        'order',
        'product',
        'quantity',
        'price'
    )