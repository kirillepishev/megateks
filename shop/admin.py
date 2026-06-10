from django.contrib import admin
from .models import Category, Product, Order, OrderItem, EmployeeProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock_quantity', 'is_active')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price_at_time')
    list_filter = ('order__status',)

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'phone')
    search_fields = ('user__username', 'position')