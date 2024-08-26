from django.shortcuts import render, get_object_or_404
from .models import Book

# Create your views here.
def book_details(request, id):
    book = get_object_or_404(Book, id=id)

    context = {
        'book_detail':book
    }

    return render(request, 'book/book_details.html', context)