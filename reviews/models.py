

from django.db import models
from django.contrib.auth.models import User
from books.models import Book


# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [
        (1, "1 Stars"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    
    rating = models.IntegerField(choices = RATING_CHOICES)
    
    comment = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "book")
        
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"