from django.shortcuts import render
from books.models import Book
from django.db.models import Count

def home(request):
    new_books = Book.objects.order_by('-created_at')[:4]

    most_borrowed_books = Book.objects.annotate(
        borrow_count=Count('borrowbook__books')
    ).order_by('-borrow_count')[:8] 

    context = {
        'books':new_books,
        'featured_books': most_borrowed_books
    }
    return render(request,'home.html',context)