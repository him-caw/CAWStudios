from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Cinema, Movie, ShowTime, Booking
from .serializers import MovieSerializer, CinemaSerializer, ShowTimeSerializer, BookingSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from django.db.models import Q

# Create your views here.

def welcome(request):
    if request.method == "POST":
        print(JSONParser().parse(request))
        return HttpResponse("Welcome to ticket booking app")


@api_view(['GET', 'POST'])
def movies(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        movie_name = request.query_params.get('movie_name', None)

        if movie_name is not None:
            movies = movies.filter(movie_name__icontains=movie_name)

        movie_serializer = MovieSerializer(movies, many=True)
        return JsonResponse(movie_serializer.data, safe=False)

    elif request.method == 'POST':
        movie_data = JSONParser().parse(request)
        movie_serializer = MovieSerializer(data=movie_data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return JsonResponse(movie_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(movie_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def cinema(request):
    if request.method == 'GET':
        cinemas = Cinema.objects.all()
        city = request.query_params.get('city', None)

        if city is not None:
            cinemas = cinemas.filter(city__icontains=city)

        cinema_serializer = CinemaSerializer(cinemas, many=True)
        return JsonResponse(cinema_serializer.data, safe=False)

    elif request.method == 'POST':
        cinema_data = JSONParser().parse(request)
        cinema_serializer = CinemaSerializer(data=cinema_data)
        if cinema_serializer.is_valid():
            cinema_serializer.save()
            return JsonResponse(cinema_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(cinema_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def showtimes(request):
    if request.method == 'GET':
        showtimes = ShowTime.objects.all()

        cine_id = request.query_params.get('cine_id', None)

        if cine_id is not None:
            showtimes = showtimes.filter(cinema_id=cine_id)
        
        movie_id = request.query_params.get('movie_id', None)

        if movie_id is not None:
            showtimes = showtimes.filter(movie_id=movie_id)

        showtime_serializer = ShowTimeSerializer(showtimes, many=True)
        return JsonResponse(showtime_serializer.data, safe=False)

    elif request.method == 'POST':
        showtime_data = JSONParser().parse(request)
        movie = Movie.objects.get(id=showtime_data['movie_id'])

        cinema = Cinema.objects.get(id=showtime_data['cinema_id'])

        if showtime_data['total_seats'] > cinema.capacity:
            return HttpResponse("Error : Cinema does not hold that capacity", status=status.HTTP_409_CONFLICT)
        
        showtime_serializer = ShowTimeSerializer(data=showtime_data)
        if showtime_serializer.is_valid():
            showtime_serializer.save()
            return JsonResponse(showtime_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(showtime_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def ongoing_shows(request):
    if request.method == 'GET':
        showtimes = ShowTime.objects.all()

        curr_time = datetime.utcnow()
        showtimes = showtimes.filter(Q(show_time__lt=curr_time), Q(end_time__gt=curr_time))

        cine_id = request.query_params.get('cine_id', None)

        if cine_id is not None:
            showtimes = showtimes.filter(cinema_id=cine_id)
        
        movie_id = request.query_params.get('movie_id', None)

        if movie_id is not None:
            showtimes = showtimes.filter(movie_id=movie_id)

        showtime_serializer = ShowTimeSerializer(showtimes, many=True)
        return JsonResponse(showtime_serializer.data, safe=False)