from django.db.models import fields
from rest_framework import serializers
from .models import Cinema, Movie, ShowTime


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

        extra_kwargs = {
            'seats_booked': {'read_only': True}
            }

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShowTime
        fields = '__all__'