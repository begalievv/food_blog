from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, FormView

from .models import PostImage
from .likes import *
from .forms import *


def post_list(request):
    search_query = request.GET.get("search", "")
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 2)
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
        'posts': page.object_list,
        "page_object": page,
        "is_paginated": is_paginated,
        "next_url": next_url,
        "prev_url": prev_url,
    }

    return render(request, "posts/home.html", context)


class PostDetailView(FormView, DetailView):
    template_name = 'posts/post_detail.html'
    model = Post
    form_class = CommentForm

    def form_valid(self, form):
        form = form.save(commit=False)
        form.user_name = self.request.user
        form.post = Post.objects.get(pk=self.kwargs['pk'])
        form.save()
        return super(PostDetailView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['likes'] = get_fans(Post.objects.get(pk=self.kwargs['pk']))
        return context

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})


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
    fields = ('body',)

    def form_valid(self, form):
        form = form.save(commit=False)
        print(self.kwargs)
        form.post = Post.objects.get(slug=self.kwargs['slug'])
        form.save()


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
    fields = ('image',)

    def form_valid(self, form):
        form = form.save(commit=False)
        print(self.kwargs)
        form.post = Post.objects.get(pk=self.kwargs['pk'])
        form.save()
        return HttpResponseRedirect('/')


def like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        add_like(obj, request.user)
        obj.status_like = True
        obj.save()
        return redirect('post_list')


def remove_like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        remove_like(obj, request.user)
        obj.status_like = False
        obj.save()
        return redirect('post_list')




