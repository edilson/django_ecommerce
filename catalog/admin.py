from django.contrib import admin

from .models import Category, Product

class CustomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created', 'modified')
    list_filter = ('name', 'slug', 'created')
    search_fields = ('name',)

class CustomProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'price', 'category', 'created', 'modified')
    list_filter = ('name', 'price', 'category', 'created')
    search_fields = ('name', 'price', 'category__name',)

admin.site.register(Category, CustomCategoryAdmin)
admin.site.register(Product, CustomProductAdmin)
