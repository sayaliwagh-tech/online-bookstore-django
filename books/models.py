


from django.db import models
from django.contrib.auth.models import User


from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
# Author model
class Author(models.Model):
    name = models.CharField(max_length=150)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to="authors/", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
# Book Model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    description = models.TextField()
    
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    stock = models.PositiveIntegerField(default=0)
    
    image  = models.ImageField(
        upload_to="books/",
        blank=True,
        null=True
        )
    
    isbn = models.CharField(max_length=13, unique=True)
    
    publication_date = models.DateField(auto_now_add=True)
    
    # new_books = Book.objects.order_by("-id")[:8]
    
    def __str__(self):
        return self.title
    

    @property
    def subtotal(self):
        return self.book.price * self.quantity