

from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.core.paginator import Paginator
from django.db.models import Q
from reviews.models import Review
from reviews.forms import ReviewForm
from django.shortcuts import redirect
from django.db.models import Avg
from wishlist.models import Wishlist

# Create your views here.

from .models import Book

def home(request):
    books = Book.objects.select_related(
        "author",
        "category"
    ).annotate(
        average_rating=Avg("reviews__rating")
    )

    featured_books = books[:8]
    new_books = books.order_by("-publication_date")[:8]

    categories = Category.objects.all()
    
    wishlist_books = []

    if request.user.is_authenticated:
        wishlist_books = Wishlist.objects.filter(
            user=request.user
        ).values_list("book_id", flat=True)
    
    return render(request, "books/home.html", {
        "featured_books": featured_books,
        "new_books": new_books,
        "categories": categories,
        "wishlist_books": wishlist_books,
    })
    
# book detail
def book_detail(request, id):
    
    book = get_object_or_404(Book, id=id)
    
    reviews = book.reviews.all()
    
    if request.method == "POST":
        
        if request.user.is_authenticated:
            
            form = ReviewForm(request.POST)
            
            if form.is_valid():
                
                review = form.save(commit=False)
                review.user = request.user
                review.book = book
                review.save()
                
    
                return redirect("book_detail", id=book.id)
        
        else:
            return redirect("login")
    
    else:
        form = ReviewForm()
        
    return render(request, 
                  "books/book_detail.html", {
                    "book": book,
                    "reviews": reviews,
                    "form": form
                  })
    
# book list
def book_list(request):
    books = Book.objects.annotate(
    average_rating=Avg("reviews__rating")
    )
    categories = Category.objects.all()
    
    # 
    wishlist_books = []

    # if request.user.is_authenticated:
    #     wishlist_books = Wishlist.objects.filter(
    #         user=request.user
    #     ).values_list("book_id", flat=True)
    
    if request.user.is_authenticated:
        wishlist_books = list(
            Wishlist.objects.filter(
                user=request.user
            ).values_list("book_id", flat=True)
        )
        
        
    
    
    # Search
    search = request.GET.get("search")
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__name__icontains=search) |
            Q(category__name__icontains=search)
        )
        
    # Cartegory Filter
    category = request.GET.get("category")
    if category:
        books = books.filter(category_id=category)
    
    
        
    # Sorting
    sort = request.GET.get("sort")
    
    if sort == "low":
        books = books.order_by("price")
        
    elif sort == "high":
        books = books.order_by("-price")
        
    # pagination
    paginator = Paginator(books, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return render(request, "books/book_list.html", {
        "page_obj": page_obj,
        "categories": categories,
        "search": search,
        "selected_category": category,
        "sort": sort,
        "wishlist_books": wishlist_books,
    })


# category_list
def category_list(request):
    categories = Category.objects.all()
    
    return render(
        request,
        "books/categories.html",
        {
            "categories": categories
        }
    )

