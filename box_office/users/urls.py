from django.urls import path
from users import views

urlpatterns = [
    path('create_user/', views.create_user, name="create_user"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('register_user', views.register_user, name="register_user"),
    path('user_profile/', views.profile_view, name="user_profile"),

]