

from django.db import models
from django.contrib.auth.models import User
from books.models import Book

from django.utils import timezone
from datetime import timedelta


# Create your models here.

def default_delivery():
    return timezone.now().date() + timedelta(days=5)

estimated_delivery = models.DateField(
    default=default_delivery
)




class Order(models.Model):

    STATUS_CHOICES = (
        ("Processing", "Processing"),
        ("Confirmed", "Confirmed"),
        ("Packed", "Packed"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    shipping_address = models.TextField()

    phone = models.CharField(max_length=15)
    
    payment_status = models.CharField(
            max_length=20,
            default="Pending"
        )
    
    payment_id = models.CharField(
            max_length=200,
            blank=True,
            null=True
        )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )
    
    estimated_delivery = models.DateField(
        default=default_delivery
    )

    def __str__(self):
        return f"Order #{self.id}"
    
    
# 
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete = models.CASCADE,
        related_name = "items"
    )
    
    book = models.ForeignKey(
        Book,
        on_delete = models.CASCADE
    )
    
    quantity = models.PositiveIntegerField()
    
    price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2
    )
    
    def __str__(self):
        return self.book.title
    
# 
