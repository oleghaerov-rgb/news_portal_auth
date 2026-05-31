from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),

    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('news/add/', views.news_create_view, name='news_create'),
    path('news/<int:news_id>/edit/', views.news_edit_view, name='news_edit'),
    path('news/<int:news_id>/delete/', views.news_delete_view, name='news_delete'),

    path('register/', views.register_view, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('profile/', views.profile_view, name='profile'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
]
