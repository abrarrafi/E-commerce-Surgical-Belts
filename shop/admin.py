from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    ordering = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'category', 'price', 'discount_price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'category', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    ordering = ['-created_at']
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


from django.contrib import admin
from .models import Product, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'city', 'zip_code', 'total_price', 'created_at')
    list_filter = ('created_at', 'city')
    search_fields = ('full_name', 'email', 'phone', 'address', 'city', 'zip_code')
    inlines = [OrderItemInline]

