from django.urls import path

from . import views

book_patterns = (
    [
        path('', views.list, name='list'),
        path('create', views.create, name='create'),
        path('update/<str:pk>', views.update, name='update'),
        path('delete/<str:pk>', views.delete, name='delete'),
        path('update/json-get-book-by-id/<str:pk>', views.json_get_book_by_id, name='json'),
    ],
    'book'
)
