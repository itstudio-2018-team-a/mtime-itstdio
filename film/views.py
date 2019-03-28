from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from . import models
import json
# Create your views here.


def get_film_list(request):
    if request.method == 'GET':
        pass
    else:
        HttpResponse(status=404)


def get_hot_film(request):
    if request.method == 'GET':
        hot_movies = models.Film.objects.all().order_by('-hits', '-create_time')[:10]

        json_data = json.dumps(hot_movies)

        HttpResponse(json_data)
    else:
        HttpResponse(status=404)


def get_on_movie_list(request):
    if request.method == 'GET':
        all_movies = models.Film.objects.all()
        ##########################

    else:
        HttpResponse(status=404)


def get_coming_movie_list(request):
    if request.method == 'GET':
        pass
    else:
        HttpResponse(status=404)


def get_film(request):
    if request.method == 'GET':
        pass
    else:
        HttpResponse(status=404)


def mark_movie(request):
    if request.method == 'POST':
        pass
    else:
        HttpResponse(status=404)


def comment_on_film(request):
    if request.method == 'POST':
        pass
    else:
        HttpResponse(status=404)







