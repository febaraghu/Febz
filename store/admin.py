from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Wishlist, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'audience', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_featured', 'is_new_arrival']
    list_filter = ['category', 'is_featured', 'is_new_arrival']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_featured', 'is_new_arrival']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'total_amount', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
    inlines = [OrderItemInline]

admin.site.register(Wishlist)
admin.site.register(Review)
