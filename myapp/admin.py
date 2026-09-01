from django.contrib import admin
from .models import client_message, Prescription, DoctorAppointment, Product, Wishlist, CartItem, Order, OrderItem

# Register your models here.

@admin.register(client_message)
class ClientMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'subject')


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'mobile_number', 'email', 'created_at')
    ordering = ('-created_at',)


@admin.register(DoctorAppointment)
class DoctorAppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'doctor', 'appointment_date', 'appointment_time', 'created_at')
    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'old_price', 'tag', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'tag', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_active')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')
    list_filter = ('added_at',)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'added_at')
    list_filter = ('added_at',)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal')
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone_number', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    list_editable = ('status',)
    search_fields = ('full_name', 'phone_number', 'email', 'id')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    readonly_fields = ('user', 'full_name', 'phone_number', 'email', 'delivery_address', 'payment_method', 'total_amount', 'created_at')
