from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Order, Transaction, Product

def login_view(request):
    next_url = request.GET.get('next', '/accounts/dashboard/')
    if request.user.is_authenticated:
        return redirect(next_url)
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect(next_url)
    else:
        form = AuthenticationForm()
        
    context = {
        'form': form,
        'page_title': 'Sign In',
    }
    return render(request, 'accounts/login.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('my_dashboard')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('my_dashboard')
    else:
        form = UserCreationForm()
        
    context = {
        'form': form,
        'page_title': 'Sign Up',
    }
    return render(request, 'accounts/register.html', context)

def logout_view(request):
    auth_logout(request)
    return redirect('index')

@login_required
def my_dashboard(request):
    order_count = Order.objects.filter(user=request.user).count()
    context = {
        'page_title': 'My Dashboard',
        'order_count': order_count,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'page_title': 'My Orders',
        'orders': orders,
    }
    return render(request, 'accounts/orders.html', context)

def my_coupons(request):
    context = {
        'page_title': 'My Coupons',
    }
    return render(request, 'accounts/coupons.html', context)


@login_required
def order_detail(request, order_code):
    order = get_object_or_404(Order, order_code=order_code, user=request.user)
    items = order.items.all()
    transaction = Transaction.objects.filter(order=order).first()
    context = {
        'page_title': f'Order Details #{order.order_code}',
        'order': order,
        'items': items,
        'transaction': transaction,
    }
    return render(request, 'accounts/order_detail.html', context)


def my_wishlist(request):
    wishlist = request.session.get('wishlist', [])
    wishlist = [int(x) for x in wishlist]
    wishlist_items = Product.objects.filter(id__in=wishlist)
    context = {
        'page_title': 'My Wishlist',
        'wishlist_items': wishlist_items,
    }
    return render(request, 'accounts/wishlist.html', context)


def add_to_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    wishlist = [int(x) for x in wishlist]
    p_id = int(product_id)
    if p_id not in wishlist:
        wishlist.append(p_id)
        request.session['wishlist'] = wishlist
        messages.success(request, 'Product added to wishlist!')
    else:
        messages.info(request, 'Product is already in your wishlist.')
    
    next_url = request.META.get('HTTP_REFERER', '/shop/')
    return redirect(next_url)


def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    wishlist = [int(x) for x in wishlist]
    p_id = int(product_id)
    if p_id in wishlist:
        wishlist.remove(p_id)
        request.session['wishlist'] = wishlist
        messages.success(request, 'Product removed from wishlist.')
    
    next_url = request.META.get('HTTP_REFERER', '/accounts/wishlist/')
    return redirect(next_url)
