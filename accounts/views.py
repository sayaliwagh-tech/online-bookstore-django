from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm, RegisterForm

from orders.models import Order

from cart.models import Cart
from wishlist.models import Wishlist
from orders.models import Order


# 
def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect("home")

    else:

        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form
    })


# 
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("home")

    return render(request, "accounts/login.html")



# 
def user_logout(request):

    logout(request)

    return redirect("home")


# 
@login_required
def profile(request):
    user = request.user
    
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={
            "full_name": user.username
        }
    )

    order_count = Order.objects.filter(user=user).count()
    wishlist_count = Wishlist.objects.filter(user=user).count()
    cart_count = Cart.objects.filter(user=user).count()

    return render(request, "accounts/profile.html", {
        "profile": profile,
        "order_count": order_count,
        "wishlist_count": wishlist_count,
        "cart_count": cart_count,
    })
        
# 
@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "full_name": request.user.username
        }
    )

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/edit_profile.html", {
        "form": form
    })