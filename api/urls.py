from django.urls import path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('login/', views.Login.as_view(), name="login"),
    path('change-password/', views.ChangePassword.as_view(), name="change-password"),
    path('register/', views.Register.as_view(), name="register"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('posts/', views.PostView.as_view(), name="posts"),
    path('posts/<int:post_id>', views.PostView.as_view(), name="posts"),
    path('portfolio/<int:work_id>', views.PortfolioView.as_view(), name="portfolio"),
    path('portfolio/', views.PortfolioView.as_view(), name="portfolio"),
    path('posts-list/<int:post_id>', views.PostList.as_view(), name="posts-list"),
    path('posts-list/', views.PostList.as_view(), name="posts-list"),
    path('works-list/', views.WorkList.as_view(), name="works-list"),
    path('works-list/<int:work_id>', views.WorkList.as_view(), name="works-list"),
]
