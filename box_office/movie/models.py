from django.db import models
from datetime import datetime, date

class Movie(models.Model):
    movie_name = models.CharField(max_length=50)
    movie_author = models.CharField(max_length=30)
    view = models.IntegerField(default=0)
    description = models.CharField(max_length=800)
    imdb_rate = models.FloatField()
    release_date = models.IntegerField()

    def __str__(self):
        return self.movie_name

class BoxOffice(models.Model):
    # movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=50)
    worldwide_gross = models.IntegerField(default=0)
    domestic_gross = models.IntegerField(default=0)
    domestic_gross_per = models.FloatField(default=0)
    foreign_gross = models.IntegerField(default=0)
    foreign_gross_per = models.FloatField(default=0)
    description = models.CharField(max_length=800, default=0)
    imdb_rate = models.FloatField(default=0)
    release_date = models.IntegerField(default=0)
    scrap_time = models.DateTimeField(default=date.today)


    def __str__(self):
        return self.movie_name


class Review(models.Model):
    question = models.ForeignKey(Movie, on_delete=models.CASCADE)
    review_text = models.CharField(max_length=1000)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.review_text