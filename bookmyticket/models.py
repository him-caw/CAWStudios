from django.db import models
from django.db.models.base import Model

# Create your models here.

class Movie(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    movie_name = models.CharField(max_length=32, unique=True)
    genre = models.CharField(max_length=32)
    release_date = models.DateField(null=False)
    starring = models.TextField()

    def __str__(self) -> str:
        return self.movie_name

class Cinema(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=32, null=False)
    address = models.TextField()
    capacity = models.IntegerField()

    def __str__(self) -> str:
        return self.name

class ShowTime(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    cinema_id = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seats_available = models.IntegerField(null=False)
    show_time = models.DateTimeField(null=False)
    total_seats = models.IntegerField()
    ticket_price = models.FloatField(null=False)

    def __str__(self) -> str:
        return self.id

class Booking(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True)
    person_name = models.CharField(null=False, max_length=16)
    qty = models.IntegerField(null=False, default=1)
    total_amt = models.IntegerField(null=False)
    show = models.ForeignKey(ShowTime, on_delete=models.CASCADE)



