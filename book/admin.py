from django.contrib import admin

from book.forms import BookForm
from book.models import Book, Category


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    form = BookForm
