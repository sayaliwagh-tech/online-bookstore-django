

from django.contrib import admin
from .models import Book, Category, Author
# from cart.models import Cart, CartItem


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "category",
        "price",
        "stock",
    )
    
    list_filter = ("category", "author")
    search_fields = ("title", "isbn")


