from django.contrib import admin
from book.models import Book


@admin.register(Book)
class AdminBook(admin.ModelAdmin):
    pass
