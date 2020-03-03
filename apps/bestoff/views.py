from django.shortcuts import render
from django.views.generic import ListView


from apps.posts.models import Post


def best_of_list(request):
    postss = Post.objects.order_by('likes')
    posts = list(set(postss))
    print(posts)
    return render(request, 'bestoff/best_of_list.html', {'posts': posts})
