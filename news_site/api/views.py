from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from api.models import ArticleInfo, Topic
from django.core import serializers

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the test api.")


@api_view(['GET'])  # how to load more?
def get_articles(request):

	topics = []	
	for topic in Topic.objects.all():
		articles = []
		for a in ArticleInfo.objects.all().filter(topic_id=topic):
			articles.append(_model_to_dict(a))
		topic_list_tuple = (_model_to_dict(topic), articles)
		topics.append(topic_list_tuple)


	# for a in ArticleInfo.objects.all():
	# 	print(a.__dict__)

	# arr = []
	# for a in ArticleInfo.objects.all():
	# 	arr.append(a)
	# print(arr)
	# request should have user ID, maybe dates
	
	return JsonResponse(topics, safe=False)

def _model_to_dict(model):
	dic = model.__dict__
	del dic['_state']
	return dic