import os
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Category, Product, Review


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    search_query = ""
    image_search_name = ""

    # Check for image search upload
    if request.method == 'POST' and 'camera_image' in request.FILES:
        camera_image = request.FILES['camera_image']
        filename = camera_image.name
        # Clean name by removing extension and separating words
        basename = os.path.splitext(filename)[0]
        image_search_name = basename.replace('_', ' ').replace('-', ' ')
        
        words = image_search_name.split()
        if words:
            query = Q()
            for word in words:
                query |= Q(name__icontains=word) | Q(description__icontains=word)
            products = products.filter(query)
        search_query = f"Uploaded Image ({filename})"
    else:
        # Check for text query search
        q = request.GET.get('q', '').strip()
        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
            search_query = q

    context = {
        'page_title': 'Shop',
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'image_search_name': image_search_name,
    }
    return render(request, 'shop.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    categories = Category.objects.all()
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    # Fetch reviews
    reviews = product.reviews.all().order_by('-created_at')
    
    # Calculate average rating
    avg_rating = 0
    if reviews.exists():
        avg_rating = sum(r.rating for r in reviews) / reviews.count()
        
    context = {
        'product': product,
        'categories': categories,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'avg_rating_int': int(round(avg_rating)),
        'page_title': product.name,
    }
    return render(request, 'single.html', context)


@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        rating = request.POST.get('rating', 5)
        comment = request.POST.get('comment', '').strip()
        
        if comment:
            Review.objects.create(
                product=product,
                user=request.user,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Review submitted successfully!')
        else:
            messages.error(request, 'Comment field cannot be empty.')
            
    return redirect('product_detail', product_id=product_id)


def bestsellers(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_bestseller=True)
    if not products.exists():
        products = Product.objects.all()
    context = {
        'page_title': 'Bestsellers',
        'categories': categories,
        'products': products,
    }
    return render(request, 'bestseller.html', context)

