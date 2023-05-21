from django.urls import path
from . import views
# Create your views here.
urlpatterns = [
    path('profile/<username>/', views.profile_with_like_movies),
    path('profile/<username>/comment/', views.profile_with_comment),
    path('profile/', views.get_my_profile),
    path('profile/<username>/follow/', views.follow),
    path('profile/<username>/update/', views.update_profile),
]