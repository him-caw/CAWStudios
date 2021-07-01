from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .models import Cinema, Movie, ShowTime, Booking
from .serializers import CinemaSerialzierWithShows, MovieSerializer, CinemaSerializer, RegisterSerializer, ShowTimeDetailSerializer, ShowTimeSerializer, BookingSerializer, MyTokenObtainPairSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from datetime import datetime
from django.db.models import Q
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Create your views here.

def welcome(request):
    if request.method == "POST":
        print(JSONParser().parse(request))
        return HttpResponse("Welcome to ticket booking app")


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
def ongoing_shows(request):
    if request.method == 'GET':
        showtimes = ShowTime.objects.all()

        curr_time = datetime.utcnow()
        showtimes = showtimes.filter(Q(show_time__lt=curr_time), Q(end_time__gt=curr_time))

        cine_city = request.query_params.get('cine_city', None)

        if cine_city is not None:
            showtimes = showtimes.filter(cinema__city__icontains=cine_city)
        
        movie = request.query_params.get('movie', None)

        if movie is not None:
            showtimes = showtimes.filter(movie__movie_name__icontains=movie)

        showtime_serializer = ShowTimeSerializer(showtimes, many=True)
        return JsonResponse(showtime_serializer.data, safe=False)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking(request):
    if request.method == 'GET':
        book_id = request.query_params.get('book_id', None)

        if book_id is None:
            return HttpResponse("Invalid Booking Id", status=status.HTTP_409_CONFLICT)

        booking = Booking.objects.get(id=book_id)

        booking_serializer = BookingSerializer(booking)
        return JsonResponse(booking_serializer.data, safe=False)

    elif request.method == 'POST':
        booking_data = JSONParser().parse(request)
        showtime = ShowTime.objects.get(id=booking_data['show'])

        if booking_data['qty'] > (showtime.total_seats - showtime.seats_booked):
            return HttpResponse("Error : No seats Available", status=status.HTTP_409_CONFLICT)

        booking_data['total_amt'] = showtime.ticket_price * booking_data['qty']
        showtime.seats_booked = showtime.seats_booked + booking_data['qty']
        showtime.save()
        
        booking_serializer = BookingSerializer(data=booking_data)
        if booking_serializer.is_valid():
            booking_serializer.save()
            return JsonResponse(booking_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(booking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getshows(request):
    if request.method == 'GET':
        showtimes = ShowTime.objects.all()
        city = request.query_params.get('city', None)

        if city is not None:
            showtimes = showtimes.filter(cinema__city__icontains=city)

        movie = request.query_params.get('movie', None)

        if movie is not None:
            showtimes = showtimes.filter(movie__movie_name__icontains=movie)

        showtimedetail_serializer = ShowTimeDetailSerializer(showtimes, many=True)
        return JsonResponse(showtimedetail_serializer.data, safe=False)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cinemas(request):
    if request.method == 'GET':
        cinemas = Cinema.objects.all()
        movie = request.query_params.get('movie', None)

        if movie is not None:
            cinemas = cinemas.filter(showtimes__movie__movie_name__icontains=movie).distinct()

        cinemadetailserializer = CinemaSerialzierWithShows(cinemas, many=True)
        return JsonResponse(cinemadetailserializer.data, safe=False)

def register_user(request):
    # user_data = JSONParser().parse(request)
    # userName = user_data['username']
    # userPass = user_data['password']
    # userMail = user_data['email']

    # if userName and userPass and userMail:
    #     u = User.objects.create_user(username = userName, email =userMail, password = userPass)
    #     return HttpResponse("Created Successfully", status=status.HTTP_200_OK)
    # else:
    #    # request was empty
    #     return HttpResponse("Fields Mandatory", status=status.HTTP_409_CONFLICT)
    if request.method == 'POST':
        
        user_data = JSONParser().parse(request)


        register_serializer = RegisterSerializer(data=user_data)
        if register_serializer.is_valid():
            register_serializer.save()
            return JsonResponse(register_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(register_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer