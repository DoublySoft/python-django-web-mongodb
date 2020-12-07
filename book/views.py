from bson import ObjectId
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .models import Book, Category
from .forms import BookForm


def index(request):
    return list_book(request, BookForm())


def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            return list_book(request, form)

    return redirect('book:list')


def update(request, pk):
    book = Book.objects.get(pk=ObjectId(pk))

    if request.method == 'POST':
        # request.POST._mutable = True
        # request.POST['category'] = ObjectId(request.POST['category'])
        # book.category = Category.objects.get(pk=ObjectId(request.POST['category']))
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
        else:
            return list_book(request, form)

    return redirect('book:list')


def list_book(request, form):
    page_number = request.GET.get('page')

    paginator = Paginator(Book.objects.all(), 4)
    books = paginator.get_page(page_number)

    return render(request, 'book/book_list.html', {'books': books, 'form': form})


def json_get_book_by_id(request, pk):
    try:
        book = Book.objects.get(pk=ObjectId(pk))
    except Book.DoesNotExist:
        return JsonResponse('')

    print(book.category.pk)

    return JsonResponse({
        'name': book.name,
        'content': book.content,
        'category': str(book.category.pk)
    })


def delete(request, pk):
    try:
        book = Book.objects.get(pk=ObjectId(pk))
        book.delete()
    except Book.DoesNotExist:
        pass

    return redirect('book:list')
