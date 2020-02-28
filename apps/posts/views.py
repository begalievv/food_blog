from django.shortcuts import render
from django.views.generic import ListView, View, TemplateView
from django.http import HttpResponse

class PostsListView(TemplateView):
    template_name = 'posts/base.html'