from django.db import models
from accounts.models import Account

# Create your models here.
class BookCategory(models.Model):
    cat_Title = models.CharField(max_length=100)
    cat_desc = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.cat_Title

class Book(models.Model):
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    images = models.ImageField(upload_to='photos/books')
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    borrow_price = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class BorrowBook(models.Model):
    user = models.ForeignKey(Account, on_delete= models.CASCADE)
    books = models.ManyToManyField(Book)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_books(self):
        return self.books.count()

    def __str__(self):
        return f"{self.user.first_name}'s Borrow"
