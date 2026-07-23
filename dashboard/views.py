from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User

from books.models import Book
from orders.models import Order
from reviews.models import Review
from wishlist.models import Wishlist

from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth


@staff_member_required
def dashboard(request):

    total_users = User.objects.count()

    total_books = Book.objects.count()

    total_orders = Order.objects.count()

    total_reviews = Review.objects.count()

    total_wishlist = Wishlist.objects.count()

    revenue = Order.objects.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    context = {
        "users": total_users,
        "books": total_books,
        "orders": total_orders,
        "reviews": total_reviews,
        "wishlist": total_wishlist,
        "revenue": revenue,
    }

    return render(
        request,
        "dashboard/dashboard.html",
        context
    )