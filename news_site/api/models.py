import uuid
from django.db import models

class ArticleInfo(models.Model):
	summary = models.TextField()
	article_url = models.URLField(max_length=150)
	video_url = models.URLField(max_length=150)
	image_url = models.URLField(max_length=150)
	date = models.DateField()
	author = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	article_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE)

class Topic(models.Model):

	topic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	topic_name = models.CharField(max_length=50)
	category_name = models.CharField(max_length=20)
	hotness_score = models.SmallIntegerField(default=0)
