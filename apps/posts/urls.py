from django.urls import path

from .views import *


urlpatterns = [
    path('', PostsListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('new/', PostCreateView.as_view(), name='post_new'),
]
