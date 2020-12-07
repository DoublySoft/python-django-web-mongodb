from django.contrib import admin
from book.models import Book, Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    pass
