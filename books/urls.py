

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name="book_list"),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path("categories/", views.category_list, name='categories'),
]
