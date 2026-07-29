from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from blog.models import BlogPost

def home(request):
    products = Product.objects.all()
    bestseller_products = Product.objects.filter(is_bestseller=True)
    new_products = Product.objects.filter(is_new=True)
    categories = Category.objects.all()
    blog_posts = BlogPost.objects.all()[:3]
    
    # Chunk products in groups of 4 for the nested mini-carousels
    products_list = list(products)
    chunked_products = [products_list[i:i + 4] for i in range(0, len(products_list), 4)]
    
    context = {
        'products': products,
        'bestseller_products': bestseller_products,
        'new_products': new_products,
        'categories': categories,
        'chunked_products': chunked_products,
        'blog_posts': blog_posts,
    }
    return render(request, 'index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        messages.success(request, f"Thank you{', ' + name if name else ''}! Your message has been sent successfully. We will contact you soon.")
        return redirect('contact')
    return render(request, 'contact.html')

def help_center(request):
    return render(request, 'help.html')

# ============ CATEGORY CRUD ============

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/category_list.html', {
        'categories': categories,
        'page_title': 'Categories',
    })

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/category_form.html', {
        'form': form,
        'page_title': 'Add Category',
    })

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/category_form.html', {
        'form': form,
        'page_title': 'Edit Category',
    })

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'admin_panel/category_confirm_delete.html', {
        'category': category,
        'page_title': 'Delete Category',
    })

# ============ PRODUCT CRUD ============

def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_panel/product_list.html', {
        'products': products,
        'page_title': 'Products',
    })

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_panel/product_form.html', {
        'form': form,
        'page_title': 'Add Product',
    })

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_panel/product_form.html', {
        'form': form,
        'page_title': 'Edit Product',
    })

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'admin_panel/product_confirm_delete.html', {
        'product': product,
        'page_title': 'Delete Product',
    })
