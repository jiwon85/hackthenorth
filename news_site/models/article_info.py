from django.db import models
from topic import Topic

class ArticleInfo(models.Model):
	summary = models.TextField()
	article_url = models.URLFIeld(max_length=150)
	video_url = models.URLField(max_length=150)
	image_url = models.URLField(max_length=150)
	date = models.DateField()
	author = models.CharField(max_length=100)
	title = models.CharField(max_length=200)
	article_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
	topic_id = models.ForeignKey(Topic, ondelete=models.CASCADE)