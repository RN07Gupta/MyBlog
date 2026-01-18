from django.urls import path
from . import views

urlpatterns = [
    # Define your URL patterns for the 'post' app here  
    path('', views.signup , name = 'signup'),
    path('signup/', views.signup , name = 'signup'),
    path('loginn/', views.loginn , name = 'loginn'),
    path('base/', views.base , name = 'base'),
    path('out/', views.out , name = 'out'),
    path('landing/', views.landing , name = 'landing'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path("profile/<str:username>/", views.user_profile, name="user_profile"),


] 