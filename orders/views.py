from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

import razorpay
from django.conf import settings

from django.http import HttpResponseBadRequest

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


# Create your views here.

@login_required
def checkout(request):

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = sum(item.subtotal for item in items)

    if request.method == "POST":

        shipping_address = request.POST.get("shipping_address")
        phone = request.POST.get("phone")

        request.session["shipping_address"] = shipping_address
        request.session["phone"] = phone

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        payment = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        return render(
            request,
            "orders/payment.html",
            {
                "payment": payment,
                "total": total,
                "razorpay_key": settings.RAZORPAY_KEY_ID,
            },
        )

    return render(
        request,
        "orders/checkout.html",
        {
            "items": items,
            "total": total,
        },
    )
    
    

@login_required
def order_success( request ):
    return render(request, 'orders/success.html')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )
    
@login_required
def payment_success(request):

    if request.method != "POST":
        return HttpResponseBadRequest("Invalid Request")

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        )
    )

    try:

        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })

    except razorpay.errors.SignatureVerificationError:
        return HttpResponseBadRequest("Payment Verification Failed")

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total = sum(item.subtotal for item in items)

    order = Order.objects.create(
        user=request.user,
        total_price=total,
        shipping_address=request.session.get("shipping_address"),
        phone=request.session.get("phone"),
        payment_status="Paid",
        payment_id=payment_id,
    )

    for item in items:
        
        if item.book.stock < item.quantity:
            return HttpResponseBadRequest(
                f"{item.book.title} is out of stock."
            )
            
        # Save order item
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price,
        )

    # Reduce stock
    item.book.stock -= item.quantity
    item.book.save()

    items.delete()

    return redirect("order_success")

# invoice
@login_required
def download_invoice(request, order_id):
    
    order = Order.objects.get(id=order_id, user=request.user)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="invoice_{order.id}.pdf"'
    )
    
    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    story = []
    
    story.append(Paragraph("<b>ONLINE BOOK STORE</b>", styles["Title"]))
    story.append(Paragraph(f"Invoice #: {order.id}", styles["Normal"]))
    story.append(Paragraph(f"Customer: {order.user.username}", styles["Normal"]))
    story.append(Paragraph(f"Phone: {order.phone}", styles["Normal"]))
    story.append(Paragraph(f"Payment Status: {order.payment_status}", styles["Normal"]))
    story.append(Paragraph(f"Total: ₹{order.total_price}", styles["Normal"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph("<b>Books Purchased:</b>", styles["Heading2"]))

    for item in order.items.all():
        story.append(
            Paragraph(
                f"{item.book.title} "
                f"(Qty: {item.quantity}) "
                f"₹{item.price}",
                styles["Normal"],
            )
        )
    
    doc.build(story)

    return response

# Cancel Order
@login_required
def cancel_order(request, id):
    
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )
    
    print(order.status)
    
    if order.status in ["Processing", "Confirmed", "Packed"]:
        order.status = "Cancelled"
        
        # Stock regain
        for item in order.items.all():
            item.book.stock += item.quantity
            item.book.save()
            
        order.save()
        
    return redirect("my_orders")

# Buy Again
@login_required
def buy_again(request, id):
    
    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )
    
    first_book = None

    for item in order.items.all():

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            book=item.book,
            defaults={
                "quantity": item.quantity
            }
        )

        if not created:
            cart_item.quantity += item.quantity
            cart_item.save()

        if first_book is None:
            first_book = item.book

    if first_book:
        return redirect("book_detail", id=first_book.id)

    return redirect("my_orders")