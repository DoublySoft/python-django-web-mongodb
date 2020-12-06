from django.contrib import admin
from django.urls import path, include

from book.urls import book_patterns

urlpatterns = [
    path('book/', include(book_patterns)),
    path('admin/', admin.site.urls),
]
