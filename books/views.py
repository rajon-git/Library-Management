from django.shortcuts import render, get_object_or_404,redirect
from .models import Book, BookCategory, BorrowBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def books(request):
    books = Book.objects.all()
    category = BookCategory.objects.all()

    context = {
        'books':books,
        'category':category
    }
    return render(request, 'book/all_books.html', context)

def book_details(request, id):
    book = get_object_or_404(Book, id=id)

    context = {
        'book_detail':book
    }

    return render(request, 'book/book_details.html', context)

@login_required
def book_borrow(request, id):
    book = get_object_or_404(Book, id=id)
    user = request.user 
    print(f"User instance: {user}")
    cart, created = BorrowBook.objects.get_or_create(user=user)
    if book in cart.books.all():
        messages.info(request, "This book is already in your cart.")
    else:
        if user.amount >= book.borrow_price:
            cart.books.add(book)
            user.amount -= book.borrow_price
            user.save()
            messages.success(request, "Book added to your cart.")
        else:
            messages.error(request, "You don't have enough money.")
            return redirect('book_detail', id=id)
    context = {
        'cart': cart
    }
    return render(request, 'author/borrow_books.html', context)

def borrow_books(request):
    return render(request, 'author/borrow_books.html')