from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'store/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully. You can now log in.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'store/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


#Product
from .models import Product
from django.db.models import Q

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {
        'products': products,
        'cart_item_count': get_cart_item_count(request)
    })


#Product detail view
from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item_count = get_cart_item_count(request)

    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_item_count': cart_item_count
    })


#Cart view
from .models import Cart, Product
from django.shortcuts import render, redirect

def get_cart_item_count(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).count()
    return 0


# View Cart
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart_item_count': get_cart_item_count(request)
    })

# Add to Cart
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        # Check if the user already has this product in the cart
        cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
        if not created:
            # If the item is already in the cart, increase the quantity
            cart_item.quantity += 1
            cart_item.save()
    else:
        # If the user is not authenticated, redirect to login page or handle as needed
        return redirect('login')  # Assuming you have a login URL
    
    # Redirect to product detail page to allow user to continue browsing or cart page
    return redirect('product_detail', product_id=product.id)

# Update Cart
def update_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        cart_item.quantity = int(request.POST.get('quantity'))
        cart_item.save()
    return redirect('view_cart')

# Remove Item from Cart
def remove_from_cart(request, cart_id):
    cart_item = Cart.objects.get(id=cart_id)
    cart_item.delete()
    return redirect('view_cart')

def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        # Here, you would typically process the order (save it to the database)
        # and create a payment flow or send an order confirmation email
        
        # For now, we just redirect to a success page
        return redirect('order_success')
    
    return render(request, 'store/checkout.html')

#order sucess 
def order_success(request):
    return render(request, 'store/order_success.html')


#about us
def about(request):
    return render(request, 'store/about.html')

#contact us
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data here (e.g., save to database or whatever else you want to do)
            
            # Display success message
            messages.success(request, 'Your message has been sent successfully!')
            
            # Redirect to contact_success page
            return redirect('contact_success')
    else:
        form = ContactForm()

    return render(request, 'store/contact.html', {'form': form})



def contact_success(request):
    return render(request, 'store/contact_success.html') 
