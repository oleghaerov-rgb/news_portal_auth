from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('news/<int:news_id>/', views.news_detail_view, name='news_detail'),
    path('news/add/', views.add_news_view, name='add_news'),
    path('news/success/', views.success_view, name='success'),
]