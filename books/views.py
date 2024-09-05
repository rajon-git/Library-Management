from django.shortcuts import render, get_object_or_404,redirect
from .models import Book, BookCategory, BorrowBook
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm 
from .models import Review
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
def books(request):
    query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    max_price_filter = request.GET.get('price_max', '')
    min_price_filter = request.GET.get('price_min', '')
    books = Book.objects.all()

    if query:
        books = books.filter(title__icontains=query) | Book.objects.filter(author__icontains=query)
    if category_filter:
        books = books.filter(category_id=category_filter)

    if min_price_filter:
        books=books.filter(borrow_price__gte=min_price_filter)
    if max_price_filter:
        books=books.filter(borrow_price__lte=max_price_filter)
    
    category = BookCategory.objects.all()

    context = {
        'books':books,
        'category':category
    }
    return render(request, 'book/all_books.html', context)

def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    reviews = book.reviews.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            if existing_review:
                messages.error(request, "You have already reviewed this book.")
            else:
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, "Review added successfully!")
                return redirect('book_details', id=id)
    else:
        form = ReviewForm()

    context = {
        'book_detail':book,
        'reviews': reviews,
        'form': form
    }

    return render(request, 'book/book_details.html', context)

@login_required
def book_borrow(request, id):
    book = get_object_or_404(Book, id=id)
    user = request.user 
    cart, created = BorrowBook.objects.get_or_create(user=user)
    if book in cart.books.all():
        messages.info(request, "This book is already you borrowed.")
        return redirect('book_details', id=id)
    else:
        if user.amount >= book.borrow_price:
            cart.books.add(book)
            user.amount -= book.borrow_price

            mail_subject = 'Borrowed booked successfully'
            message = render_to_string('email_borrow_book.html', {
                'user': user,
                'book_name': book.title,
            })
            to_email = user.email

            send_email = EmailMessage(mail_subject, message, from_email=settings.EMAIL_HOST_USER, to=[to_email])
            send_email.content_subtype = 'html'  
            send_email.send()
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