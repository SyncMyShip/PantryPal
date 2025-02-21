from django.urls import path
from .views import home, about, search, RecipeListView, RecipeDetailView, add_recipe

app_name = 'recipes'

urlpatterns = [
    path('', home),
    path('home/', home, name='home'),
    path('add/', add_recipe, name='add_recipe'),
    path('recipes/', search, name='search'),
    path('about/', about, name='about'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('list/<pk>', RecipeDetailView.as_view(), name='detail'),
]