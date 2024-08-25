from django.db import models

# Create your models here.
class BookCategory(models.Model):
    cat_Title = models.CharField(max_length=100)
    cat_desc = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.cat_Title

class Book(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    images = models.ImageField(upload_to='photos/books')
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    borrow_price = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
