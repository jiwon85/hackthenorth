from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the test api.")


@api_view(['GET'])  # how to load more?
def get_articles(request):
	data = {}
	# request should have user ID, maybe dates
	return HttpResponse(data)

