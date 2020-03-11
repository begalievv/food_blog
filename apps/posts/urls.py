from django.urls import path

from .views import *


urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('new/', PostCreateView.as_view(), name='post_new'),
    path('<int:pk>/add-photo/', PostAddPhoto.as_view(), name='add_photo'),
    path('like/<int:pk>/', like_post, name='like_post'),
    path('remove-like/<int:pk>/', remove_like_post, name='remove_like_post'),
    path('<int:pk>/add-comment/', AddComment.as_view(), name='add_comment'),
    # path('<int:pk>/likes/', PostLikes.as_view(), name='post_likes'),
]
