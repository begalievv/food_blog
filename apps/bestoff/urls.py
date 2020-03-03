from django.urls import path, include

from .views import best_of_list


urlpatterns = [
    path('', best_of_list, name='best_of_list'),
]