from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import ListView

from apps.posts.likes import *
from apps.posts.models import Post


def best_of_list(request):
    posts = Post.objects.annotate(count=Count('likes')).order_by('-count')
    return render(request, 'bestoff/best_of_list.html', {'posts': posts})


def like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        add_like(obj, request.user)
        obj.status_like = True
        obj.save()
        return redirect('best_of_list')


def remove_like_post(request, pk):
    if request.method == "POST":
        obj = Post.objects.get(pk=pk)
        remove_like(obj, request.user)
        obj.status_like = False
        obj.save()
        return redirect('best_of_list')
