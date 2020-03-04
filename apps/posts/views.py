from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, View

from .models import PostImage, Post
from .likes import *
from .forms import *


# class PostsListView(ListView):
#     template_name = 'posts/home.html'
#     model = Post


def post_list(request):
    search_query = request.GET.get("search", "")
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        posts = Post.objects.all()
    # posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = "?page={}".format(page.previous_page_number())
    else:
        prev_url = ""

    if page.has_next():
        next_url = "?page={}".format(page.next_page_number())
    else:
        next_url = ""

    context = {
        'posts': posts,
        "page_object": page,
        "is_paginated": is_paginated,
        "next_url": next_url,
        "prev_url": prev_url,
    }

    return render(request, "posts/home.html", context)


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post

    def post(self, request):
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user_name = request.user
            form.save()
        return redirect('/')



class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'posts/post_create.html'
    fields = ('title', 'description', 'category', 'author')
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AddComment(CreateView):
    model = Comment
    template_name = 'posts/post_add_comment.html'
    fields = '__all__'


class PostEditView(UpdateView):
    model = Post
    template_name = 'posts/post_update.html'
    fields = ['title', 'description',]


class PostDeleteView(DeleteView):
    template_name = 'posts/post_delete.html'
    model = Post
    success_url = reverse_lazy('post_list')


class PostAddPhoto(CreateView):
    model = PostImage
    template_name = 'posts/post_add_photo.html'
    fields = '__all__'

def like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        add_like(obj, request.user)
        return redirect('/')


def remove_like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        remove_like(obj, request.user)
        return redirect('/')
