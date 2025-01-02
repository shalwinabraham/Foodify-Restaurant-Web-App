from django.contrib import admin
from .models import FoodItem, CartItem, Order, OrderItem, TableBooking

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'ordered_at', 'is_paid', 'created_at')
    inlines = [OrderItemInline]

class TableBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_number', 'booking_time')
    search_fields = ('user__username', 'table_number')
    list_filter = ('booking_time',)

admin.site.register(FoodItem)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(TableBooking, TableBookingAdmin)
