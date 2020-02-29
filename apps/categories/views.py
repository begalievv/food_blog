from django.shortcuts import render
from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from .models import Category
from apps.posts.models import Post

class CategoriesListView(ListView):
    model = Category
    template_name = 'categories/categories_list.html'


def filter_by_cat(request, pk):
    filter_posts = Post.objects.filter(category=pk)
    return render(request, 'categories/categories_detail.html', {'filtered_posts':filter_posts})

