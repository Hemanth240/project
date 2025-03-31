from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Cart, Order, UserProfile
from .forms import ProductForm, RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate


# ✅ Home Page

def home(request):
    products = Product.objects.only('id', 'name', 'image', 'price')  # ✅ Load only necessary fields
    return render(request, 'store/home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']  # From your custom form

            # ✅ Create user with hashed password
            user = User.objects.create_user(
                username=username,
                password=password,  # This will hash the password automatically
                email=email
            )
            user.save()  # ✅ Save user to the database

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error during registration. Please correct the errors below.')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})


# ✅ User Login (Renamed to user_login)
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # ✅ Use auth_login to avoid conflict
            return redirect('home')
        else:
            messages.error(request, "❌ Invalid username or password!")
    return render(request, 'store/login.html')

# ✅ Logout Function
def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'store/profile.html', {'user_profile': user_profile})

# Product Management
def product_list(request):
    products = Product.objects.all()
    return render(request, '', {'products': products})

# ✅ Show products for a specific category
def category_products(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, '', {'category': category, 'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form})

# Cart and Checkout
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    grand_total = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total  # ✅ Ensure this is passed
    }
    return render(request, 'store/cart.html',context )

@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    return redirect('cart')


@login_required
def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.quantity += 1  # ✅ Increase quantity
    cart_item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1  # ✅ Decrease quantity
        cart_item.save()
    else:
        cart_item.delete()  # ✅ If quantity is 0, remove item
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    return render(request, 'checkout')

# Admin Panel@login_required
@login_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders
    }

    return render(request, 'store/admin_dashboard.html', context)

@login_required
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'store/manage_orders.html', {'orders': orders})

@login_required
def manage_users(request):
    return render(request, 'store/manage_users.html')