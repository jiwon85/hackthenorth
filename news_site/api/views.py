from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from api.models import ArticleInfo
from django.core import serializers

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the test api.")


@api_view(['GET'])  # how to load more?
def get_articles(request):
	data = serializers.serialize('json', ArticleInfo.objects.all())
	# arr = []
	# for a in ArticleInfo.objects.all():
	# 	arr.append(a)
	# print(arr)
	# request should have user ID, maybe dates
	
	return JsonResponse(data, safe=False)

