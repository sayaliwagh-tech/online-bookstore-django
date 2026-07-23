from django.db import models
from django.contrib.auth.models import User
from books.models import Book

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Cart"
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items"
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.book.title} ({self.quantity})"
    
    @property
    def subtotal(self):
        return self.book.price * self.quantity