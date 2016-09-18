import uuid
from django.db import models

class Topic(models.Model):
	category_name = models.CharField(max_length=20, default=None, blank=True, null=True)
	hotness_score = models.SmallIntegerField(default=0)


class ArticleInfo(models.Model):
	summary = models.TextField()
	article_url = models.URLField(max_length=150)
	video_url = models.URLField(max_length=150, default=None, blank=True, null=True)
	image_url = models.URLField(max_length=150, default=None, blank=True, null=True)
	date = models.DateField(default=None, blank=True, null=True)
	author = models.CharField(max_length=100, default=None, blank=True, null=True)
	source = models.CharField(max_length=30)
	title = models.CharField(max_length=200)

	topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
