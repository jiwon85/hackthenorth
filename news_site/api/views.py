from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from api.models import ArticleInfo, Topic
from django.core import serializers

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the test api.")


@api_view(['GET'])  # how to load more?
def get_articles(request):
    topics = _get_topic_articles({}, {})
    return JsonResponse(topics, safe=False)


def _get_topic_articles(categories_filter, source_filter):
    # Do some filtering here with regard to categories
    topics = []
    for topic in Topic.objects.all():
        articles = []
        for a in topic.articleinfo_set.all():
            articles.append(model_to_dict(a))
        topic_list_tuple = (model_to_dict(topic), articles)
        topics.append(topic_list_tuple)
    return topics


