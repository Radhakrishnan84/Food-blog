from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('publish/<int:blog_id>/', views.publish_blog, name='publish_blog'),
    path('unpublish/<int:blog_id>/', views.unpublish_blog, name='unpublish_blog'),
    path('logout/', views.logout_view, name='logout'),
]