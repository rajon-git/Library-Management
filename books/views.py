from django.shortcuts import render, get_object_or_404,redirect
from .models import Book, BookCategory, BorrowBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def books(request):
    query = request.GET.get('q', '')

    if query:
        books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    else:
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
    cart, created = BorrowBook.objects.get_or_create(user=user)
    if book in cart.books.all():
        messages.info(request, "This book is already you borrowed.")
    else:
        if user.amount >= book.borrow_price:
            cart.books.add(book)
            user.amount -= book.borrow_price
            user.save()
            messages.success(request, "Borrowed booked successfully")
            return redirect('borrow_books')
        else:
            messages.error(request, "You don't have enough money.")
            return redirect('book_details', id=id)
    context = {
        'cart': cart
    }
    return render(request, 'author/borrow_books.html', context)

@login_required
def borrow_books(request):
    user = request.user 
    borrowed_books = BorrowBook.objects.filter(user=user)
    # books = Book.objects.filter(borrowbook__in=borrowed_books).distinct()
    
    context = {
        # 'books': books,
        'borrowed_books':borrowed_books
    }
    return render(request, 'author/borrow_books.html', context)

def return_books(request,id):
    book = get_object_or_404(Book, id=id)
    user = request.user 
    borrow_store = BorrowBook.objects.get(user=user)
    if book in borrow_store.books.all():
        borrow_store.books.remove(book)
        user.amount += book.borrow_price
        user.save()
        borrow_store.save()
        messages.success(request, "Booked Return successfully")
    else:
        messages.error(request, "Book is not in your borrow record")
   
    return redirect('borrow_books')