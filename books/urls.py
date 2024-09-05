from django.urls import path
from . import views
urlpatterns = [
    path('books/',views.books, name="books"),
    path('<int:id>',views.book_details, name="book_details"),
    path('borrow/<int:id>',views.book_borrow, name="book_borrow"),
    path('borrow_books/',views.borrow_books, name="borrow_books"),
    path('return_books/<int:id>',views.return_books, name="return_books"),
]
