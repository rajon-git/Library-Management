from django.shortcuts import render
from books.models import Book

def home(request):
    books = Book.objects.all()
    context = {
        'books':books
    }
    return render(request,'home.html',context)