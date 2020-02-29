from django.urls import path
from .views import *

urlpatterns = [
    path('', CategoriesListView.as_view(), name='categories_list'),
    path('<int:pk>/', filter_by_cat, name='filter_by_category'),
]