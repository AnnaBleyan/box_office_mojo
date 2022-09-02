from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('home/', views.home, name="home_"),
    path('scrap', views.scrap, name='scrap'),
    path('movies', views.movie_list, name='movie_list'),
    path('graphic', views.graphic, name='graphic'),
    path('domestic', views.domestic_graphic, name='domestic'),
    path('domestic_per', views.domestic_percent, name='domestic_per'),
    path('foreign', views.foreign_graphic, name='foreign'),
    path('foreign_per', views.foreign_percent, name='foreign_per'),
    path('mixed', views.mixed_graphic, name='mixed'),
    path('stats', views.movie_table, name='movie_table'),
    path('movie_stat/<str:movie_name>', views.movie_stat, name='movie_stat'),
]