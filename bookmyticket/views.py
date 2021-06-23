from django.shortcuts import render, HttpResponse

# Create your views here.

def welcome(request):
    return HttpResponse("Welcome to ticket booking app")