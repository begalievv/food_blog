from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView


from apps.posts.models import Post


def best_of_list(request):
    posts = Post.objects.annotate(count=Count('likes')).order_by('-count')
    return render(request, 'bestoff/best_of_list.html', {'posts': posts})
