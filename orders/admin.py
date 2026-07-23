

from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderItem)

# 
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


# 
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "payment_status",
        "total_price",
        "created_at",
        "estimated_delivery",
    )
    
    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )
    
    search_fields = (
        "user__username",
        "phone",
        "payment_id",
    )
    
    inlines = [OrderItemInline]
   
   
# 
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "book",
        "quantity",
        "price",
    )