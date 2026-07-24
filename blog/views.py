from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost

# ============ STOREFRONT VIEWS ============

def blog_list(request):
    posts = BlogPost.objects.all()
    context = {
        'page_title': 'Blog',
        'posts': posts,
    }
    return render(request, 'blog.html', context)


def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    recent_posts = BlogPost.objects.exclude(id=post.id)[:5]
    context = {
        'page_title': post.title,
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog_detail.html', context)


# ============ ADMIN CRUD VIEWS (CBV) ============

class CreatePostView(CreateView):
    model = BlogPost
    template_name = 'Admin/Blog/create_post.html'
    fields = ['title', 'slug', 'author', 'content', 'image']
    success_url = reverse_lazy('post-list')


class PostListView(ListView):
    model = BlogPost
    template_name = 'Admin/Blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'Admin/Blog/post_detail.html'
    context_object_name = 'post'


class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'Admin/Blog/update_post.html'
    fields = ['title', 'slug', 'author', 'content', 'image']
    success_url = reverse_lazy('post-list')


class DeletePostView(DeleteView):
    model = BlogPost
    template_name = 'Admin/Blog/delete_post.html'
    success_url = reverse_lazy('post-list')
