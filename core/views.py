from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def shop(request):
    return render(request, 'shop.html')

def single(request):
    return render(request, 'single.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'cheackout.html')

def contact(request):
    return render(request, 'contact.html')

def bestsellers(request):
    return render(request, 'bestseller.html')

def page_not_found(request):
    return render(request, '404.html')
