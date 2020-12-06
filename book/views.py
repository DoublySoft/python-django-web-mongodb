from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Book
from .forms import BookForm


def index(request):
    return _listBook(request, BookForm())


def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return _listBook(request, form)

    redirect('book:index')


def _listBook(request, form):
    books = Book.objects.all()
    paginator = Paginator(books, 2)

    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)

    return render(request, 'book/index.html', {'books': books_page, 'form': form})
