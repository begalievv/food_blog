from django.urls import path, include

from .views import best_of_list, like_post, remove_like_post


urlpatterns = [
    path('', best_of_list, name='best_of_list'),
    path('like/<int:pk>/', like_post, name='like_post1'),
    path('remove-like/<int:pk>/', remove_like_post, name='remove_like_post1'),
]