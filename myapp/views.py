from django.shortcuts import render
from django.contrib import messages
from .models import client_message, Prescription, DoctorAppointment, Product, Wishlist, CartItem, Order, OrderItem
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def shop(request):
    products = Product.objects.filter(is_active=True)

    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(category=selected_category)

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    context = {
        'products': products,
        'selected_category': selected_category,
        'wishlist_ids': wishlist_ids,
    }
    return render(request,'shop.html', context)


def _category_page(request, category, template_name):
    """Shared logic for every medicine-category page (painfever, vitamins, etc.)"""
    products = Product.objects.filter(is_active=True, category=category)

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = list(
            Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        )

    context = {
        'products': products,
        'wishlist_ids': wishlist_ids,
    }
    return render(request, template_name, context)

def doctor(request):
    return render(request,'doctor.html')

def prescription(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        delivery_address = request.POST.get('delivery_address')
        additional_notes = request.POST.get('additional_notes')
        prescription_file = request.FILES.get('prescription_file')

        if not prescription_file:
            messages.error(request, 'Please upload a prescription file')
            return redirect('prescription')

        Prescription.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            email=email,
            delivery_address=delivery_address,
            prescription_file=prescription_file,
            additional_notes=additional_notes
        )

        messages.success(request, 'Prescription uploaded successfully! We will contact you shortly.')
        return redirect('prescription')

    return render(request,'prescription.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name') 
        email = request.POST.get('email') 
        phone_number = request.POST.get('phone_number') 
        message = request.POST.get('message') 
        subject = request.POST.get('subject') 

        # create a new client_message instance
        client_message.objects.create( 
            name=name,
            email=email,
            phone_number=phone_number,
            message=message,
            subject=subject
        )
        return redirect ('/')

    return render(request,'contact.html')

def painfever(request):
    return _category_page(request, 'painfever', 'painfever.html')

def vitamins(request):
    return _category_page(request, 'vitamins', 'vitamins.html')

def coldcough(request):
    return _category_page(request, 'coldcough', 'coldcough.html')

def diabetes(request):
    return _category_page(request, 'diabetes', 'diabetes.html')

def firstaid(request):
    return _category_page(request, 'firstaid', 'firstaid.html')

def skincare(request):
    return _category_page(request, 'skincare', 'skincare.html')

def babycare(request):
    return _category_page(request, 'babycare', 'babycare.html')

def devices(request):
    return _category_page(request, 'devices', 'devices.html')

def doctorappoint(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        doctor = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        problem_description = request.POST.get('problem_description')

        DoctorAppointment.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            age=age,
            gender=gender,
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            problem_description=problem_description
        )

        messages.success(request, 'Appointment booked successfully! Our doctor will contact you shortly.')
        return redirect('doctorappoint')

    return render(request,'doctorappoint.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        users = User.objects.filter(email=email)

        if not users.exists():
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'login.html')

        for user in users:
            authenticated_user = authenticate(
                request,
                username=user.username,
                password=password
            )

            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, 'Login Successful! Welcome back.')
                return redirect('home')

        messages.error(request, 'Invalid Email or Password')
    return render(request,'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username:
            messages.error(request, 'Username is required')
            return redirect('register')

        if not email:
            messages.error(request, 'Email is required')
            return redirect('register')

        if password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        messages.success(request, 'Registration Successful')
        return redirect('login')
    return render(request,'register.html')


def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='login')
@require_POST
def toggle_wishlist(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    wishlist_item = Wishlist.objects.filter(user=request.user, product=product).first()

    if wishlist_item:
        wishlist_item.delete()
        liked = False
    else:
        Wishlist.objects.create(user=request.user, product=product)
        liked = True

    wishlist_count = request.user.wishlist_items.count()

    return JsonResponse({
        'status': 'ok',
        'liked': liked,
        'wishlist_count': wishlist_count,
    })


@login_required(login_url='login')
@require_POST
def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product, defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    cart_count = sum(item.quantity for item in request.user.cart_items.all())

    return JsonResponse({
        'status': 'ok',
        'cart_count': cart_count,
        'product_quantity': cart_item.quantity,
    })


@login_required(login_url='login')
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    cart_rows = [
        {'item': item, 'subtotal': item.product.price * item.quantity}
        for item in cart_items
    ]
    total = sum(row['subtotal'] for row in cart_rows)
    return render(request, 'cart.html', {'cart_rows': cart_rows, 'total': total})


@login_required(login_url='login')
@require_POST
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    cart_count = sum(item.quantity for item in request.user.cart_items.all())
    return JsonResponse({'status': 'ok', 'cart_count': cart_count})


@login_required(login_url='login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required(login_url='login')
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart')

    cart_rows = [
        {'item': item, 'subtotal': item.product.price * item.quantity}
        for item in cart_items
    ]
    total = sum(row['subtotal'] for row in cart_rows)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        delivery_address = request.POST.get('delivery_address')
        payment_method = request.POST.get('payment_method', 'COD')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            delivery_address=delivery_address,
            payment_method=payment_method,
            total_amount=total,
        )

        for row in cart_rows:
            item = row['item']
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )

        cart_items.delete()

        messages.success(request, f'Order placed successfully! Your order ID is #{order.id}.')
        return redirect('order_success', order_id=order.id)

    context = {
        'cart_rows': cart_rows,
        'total': total,
        'default_address': getattr(request.user, 'email', ''),
    }
    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'orders.html', {'orders': orders})


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

