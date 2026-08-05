import os
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Category, Product, Review


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    search_query = ""
    image_search_name = ""
    selected_category = None

    # Check for category filter parameter
    category_id = request.GET.get('category')
    if category_id:
        try:
            selected_category = Category.objects.get(pk=category_id)
            products = products.filter(category=selected_category)
            search_query = f"Category: {selected_category.name}"
        except (Category.DoesNotExist, ValueError):
            pass

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
    elif not selected_category:
        # Check for text query search
        q = request.GET.get('q', '').strip()
        if q:
            products = products.filter(Q(name__icontains=q) | Q(description__icontains=q))
            search_query = q

    # Apply sort
    sort = request.GET.get('sort', 'default')
    if sort == 'low-high':
        products = products.order_by('price')
    elif sort == 'high-low':
        products = products.order_by('-price')
    elif sort == 'newness':
        products = products.order_by('-created_at')
    # default: no ordering override

    context = {
        'page_title': 'Shop',
        'categories': categories,
        'products': products,
        'search_query': search_query,
        'image_search_name': image_search_name,
        'selected_category': selected_category,
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
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating', 5))
        except (ValueError, TypeError):
            rating = 5

        comment = request.POST.get('comment', '').strip()

        if not comment:
            messages.error(request, 'Comment field cannot be empty.')
            return redirect('product_detail', product_id=product_id)

        word_count = len(comment.split())
        if word_count > 250:
            messages.error(request, f'Comment cannot exceed 250 words (currently {word_count} words).')
            return redirect('product_detail', product_id=product_id)

        try:
            review, created = Review.objects.get_or_create(
                product=product,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            if not created:
                review.rating = rating
                review.comment = comment

            review.full_clean()
            review.save()

            if created:
                messages.success(request, 'Review submitted successfully!')
            else:
                messages.success(request, 'Your review has been updated!')
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for err in errors:
                    messages.error(request, f"{field.capitalize()}: {err}")
        except Exception as e:
            messages.error(request, f"Error saving review: {str(e)}")

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

