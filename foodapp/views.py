from django.shortcuts import render, redirect, get_object_or_404
from .models import FoodItem, CartItem, Order, OrderItem, TableBooking
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            print(f"Account created for {username}! You can now log in.")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def intro(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'intro.html')

@login_required
def home(request):
    user = request.user
    dict1 = {
        "item": FoodItem.objects.all(),
        "user": user
    }
    return render(request, 'home.html', dict1)

@login_required
def add_to_cart(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        food_item=food_item,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{food_item.name} added to your cart.")
    return redirect('home')

@login_required
def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "The item was not found in your cart.")
    return redirect('cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.get_total_price() for item in cart_items)
    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        return redirect('cart')
    
    total_price = sum(item.food_item.price * item.quantity for item in cart_items)
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        ordered_at=None,
        is_paid=False
    )

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            food_item=cart_item.food_item,
            quantity=cart_item.quantity,
            price=cart_item.food_item.price or 0
        )
    
    cart_items.delete()
    return redirect('booking_success')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    for order in orders:
        for item in order.orderitem_set.all():
            item.price = item.price or 0
            item.total_price = item.quantity * item.price
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def clear_orders(request):
    if request.method == 'POST':
        Order.objects.filter(user=request.user).delete()
        messages.success(request, "All your orders have been cleared.")
        return redirect('my_orders')


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    messages.success(request, f"Order #{order_id} has been cancelled.")
    return redirect('my_orders')

@login_required
def booking_success(request):
    return render(request, 'booking_success.html')

@login_required
def book_table(request):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        booking_time = request.POST.get('booking_time')
        number_of_guests = request.POST.get('number_of_guests')
        TableBooking.objects.create(
            user=request.user,
            table_number=table_number,
            booking_time=booking_time,
            number_of_guests=number_of_guests
        )

        send_confirmation_email(request.user.email, table_number, booking_time, number_of_guests)
        messages.success(request, "Table booked successfully! A confirmation email has been sent.")
        return render(request, 'table_booking_success.html')

    return render(request, 'book_table.html')

def send_confirmation_email(user_email, table_number, booking_time, number_of_guests):
    subject = "Table Booking Confirmation"
    message = (f"Your table {table_number} has been booked for {booking_time}. "
               f"Number of guests: {number_of_guests}. Thank you for choosing our service!")
    from_email = "sampleemail@gmail.com"
    send_mail(subject, message, from_email, [user_email])

@login_required
def bookedtables(request):
    booked = {
        "booked_tables": TableBooking.objects.filter(user=request.user).order_by('booking_time')
    }
    return render(request, 'booked_tables.html', booked)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(TableBooking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, f"Booking for table {booking.table_number} at {booking.booking_time} has been cancelled.")
    return redirect('bookedtables')
