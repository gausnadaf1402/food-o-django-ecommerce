from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from .forms import ProductForm, RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def product_list(request):

    products = Product.objects.all()

    cart_count = 0
    wishlist_count = 0
    orders_count=0

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        orders_count = Order.objects.filter(user=request.user).count()

    context = {
        'products': products,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'orders_count':orders_count
    }

    return render(request, 'product_list.html', context)


def product_detail(request,id):

    product = Product.objects.get(id=id)

    return render(request,'product_detail.html',{'product':product})

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):

    if request.method == "POST":

        user = authenticate(
        username=request.POST['username'],
        password=request.POST['password']
        )

        if user:
            login(request,user)
            return redirect('home')

    return render(request,'login.html')


def logout_view(request):
    logout(request)
    return redirect('register')


@login_required
def add_to_cart(request,id):

    product = Product.objects.get(id=id)

    cart,created = Cart.objects.get_or_create(
    user=request.user,
    product=product
    )

    cart.quantity += 1
    cart.save()
    messages.success(request, f"{product.name} added to cart 🛒")
    return redirect('cart')


@login_required
def cart(request):

    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price*item.quantity for item in items)

    return render(request,'cart.html',{'items':items,'total':total})


@login_required
def remove_cart(request,id):

    item = Cart.objects.get(id=id)
    item.delete()
    messages.warning(request, f"{item.product} removed from cart ❌")
    return redirect('cart')


@login_required
def checkout(request):

    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price*item.quantity for item in items)

    order = Order.objects.create(user=request.user,total_price=total)

    for item in items:

        OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity
        )

    items.delete()

    return redirect('orders')


@login_required
def orders(request):

    orders = Order.objects.filter(user=request.user)

    return render(request,'orders.html',{'orders':orders})


def search(request):

    query = request.GET.get('q','').strip()
    products = Product.objects.none()
    if query:                                   
        products = Product.objects.filter(Q(name__icontains=query))
    return render(request,'product_list.html',{'products':products})

# For Custom Dashboard

def admin_products(request):
    if not request.user.is_staff:
        return redirect('/')

    products = Product.objects.all()
    return render(request,'admin_products.html',{'products':products})


def add_product(request):

    if not request.user.is_staff:
        return redirect('/')

    form = ProductForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        messages.success(request, "Product added successfully ✅")
        return redirect('/admin-products/')

    return render(request,'add_product.html',{'form':form})

def edit_product(request,id):

    product = get_object_or_404(Product,id=id)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        messages.success(request, "Product Edited successfully ✅")
        return redirect('/admin-products/')

    return render(request,'add_product.html',{'form':form})

def delete_product(request,id):

    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, "Product Deleted successfully ✅")
    return redirect('/admin-products/')

# Admin Dashboard
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect('/')

    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()

    context = {
        'products': total_products,
        'orders': total_orders,
        'users': total_users
    }

    return render(request, 'admin_dashboard.html', context)

# Wishlist logic
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    messages.success(request, f"{product.name} added to wishlist ❤️")
    return redirect('home')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()
    messages.warning(request, f"{product.name} removed from wishlist ❌")
    return redirect('wishlist')

@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'wishlist.html', {'items': items})