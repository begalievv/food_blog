from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView

from .models import PostImage, Post

class PostsListView(ListView):
    template_name = 'posts/home.html'
    model = Post


class PostDetailView(DetailView):
    template_name = 'posts/post_detail.html'
    model = Post


class PostCreateView(CreateView):
    model = Post
    template_name = 'posts/post_create.html'
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
