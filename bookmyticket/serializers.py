from django.db.models import fields
from rest_framework import serializers
from .models import Booking, Cinema, Movie, ShowTime
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class CinemaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cinema
        fields = '__all__'

class ShowTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTime
        fields = '__all__'

        # extra_kwargs = {
        #     'seats_booked': {'read_only': True}
        #     }

class ShowTimeDetailSerializer(serializers.ModelSerializer):
    cinema = CinemaSerializer()
    movie = MovieSerializer()

    class Meta:
        model = ShowTime
        fields = ('id', 'show_time', 'end_time', 'total_seats', 'seats_booked', 'cinema', 'movie')
        
class CinemaSerialzierWithShows(serializers.ModelSerializer):
    showtimes = ShowTimeDetailSerializer(many=True)

    class Meta:
        model = Cinema
        fields = ('id', 'name', 'address', 'city', 'showtimes')



class BookingSerializer(serializers.ModelSerializer):
    show = ShowTimeDetailSerializer()

    class Meta:
        model = Booking
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')

    def create(self, obj):
        user = super(RegisterSerializer, self).create(obj)
        user.set_password(obj['password'])
        user.save()
        return user

    def to_representation(self, obj):
        ret = super(RegisterSerializer, self).to_representation(obj)
        ret.pop('password')
        return ret 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token