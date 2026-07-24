from core.models import Category, Product

def categories_processor(request):
    return {
        'categories': Category.objects.all()
    }

def cart_processor(request):
    cart_session = request.session.get('cart', {})
    cart_count = sum(cart_session.values())
    subtotal = 0.0
    
    for product_id, quantity in cart_session.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal += float(product.price) * quantity
        except (Product.DoesNotExist, ValueError):
            continue
            
    return {
        'global_cart_count': cart_count,
        'global_cart_subtotal': subtotal,
    }

def wishlist_processor(request):
    wishlist = request.session.get('wishlist', [])
    wishlist = [int(x) for x in wishlist]
    return {
        'global_wishlist_count': len(wishlist),
        'wishlist_items': Product.objects.filter(id__in=wishlist)
    }
