from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict

from rest_framework.decorators import api_view
from api.models import ArticleInfo, Topic
from django.core import serializers

import json

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the test api.")


@api_view(['GET'])  # how to load more?
def get_articles(request):
    topics = _get_topic_articles(
        json.loads(request.GET.get('categories')),
        json.loads(request.GET.get('sources'))
    )
    return JsonResponse(topics, safe=False)


def _get_topic_articles(categories_filter, source_filter):
    # Do some filtering here with regard to categories
    topics = []
    for topic in Topic.objects.filter(category_name__in=categories_filter).distinct().all():

        articles = []
        articles_source = {}
        for a in topic.articleinfo_set.filter(source__in=source_filter).all():
            if a.source in articles_source:
                continue
            articles_source[a.source] = True
            articles.append(model_to_dict(a))

        if len(articles) == 0:
            continue

        topic_dict = model_to_dict(topic)
        topic_dict['hotness_score'] = len(articles)

        topic_list_tuple = (topic_dict, articles)
        topics.append(topic_list_tuple)
    return topics


