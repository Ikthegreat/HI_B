from django.urls import path
from . import views
# Create your views here.
urlpatterns = [
    path('profile/<username>/', views.user_profile),
    path('follow/<username>/', views.follow),
    path('upload_img/<username>/', views.upload_img),
]