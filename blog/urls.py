from django.urls import path
from . import views

urlpatterns = [
    path('search-api/', views.search_api, name='search_api'),
    path('', views.home, name="home"),
    path('blog/', views.blog_page, name='blog_page'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('recipes/', views.recipes_page, name='recipes_page'),
    path('recipes/all/', views.all_recipes, name='all_recipes'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('write/', views.create_blog, name='create_blog'),
    path('like/<int:blog_id>/', views.toggle_like, name='like'),
    path('comment/<int:blog_id>/', views.add_comment, name='comment'),

]