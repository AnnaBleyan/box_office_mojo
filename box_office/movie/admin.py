from django.contrib import admin
from .models import Movie, Review, BoxOffice

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(BoxOffice)