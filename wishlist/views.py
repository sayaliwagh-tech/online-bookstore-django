


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from books.models import Book


@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        book=book
    ).first()
    
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user=request.user,
            book=book
        )
        
    # Go back to the same page
    if request.META.get("HTTP_REFERER"):
        return redirect(request.META["HTTP_REFERER"])

    return redirect("home")


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, "wishlist/wishlist.html", {
        "items": items
    })


@login_required
def remove_from_wishlist(request, id):
    item = get_object_or_404(
        Wishlist,
        id=id,
        user=request.user
    )

    item.delete()

    return redirect("wishlist")


