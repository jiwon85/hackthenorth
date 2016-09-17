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

# class CategoryEnum(models.Field):

#     def __init__(self, *args, **kwargs):
#         super(CategoryEnum, self).__init__(*args, **kwargs)
#         if not self.choices:
#             raise AttributeError('EnumField requires `choices` attribute.')

#     def db_type(self):
#         return "enum(%s)" % ','.join("'%s'" % k for (k, _) in self.choices)

# CATEGORY_POLITICS = 0
# CATEGORY_SPORTS = 1
# CATEGORY_BUSINESS = 2
# CATEGORY_ENTERTAINMENT = 3
# CATEGORY_TECHNOLOGY = 4
# CATEGORY_HEALTH = 5
# CATEGORY_SCIENCE = 6
# CATEGORY_OTHER = 7

# CATEGORY_CHOICES = (
#     (CATEGORY_POLITICS, 'politics'),
#     (CATEGORY_SPORTS, 'sports'),
#     (CATEGORY_BUSINESS, 'business'),
#     (CATEGORY_ENTERTAINMENT, 'entertainent'),
#     (CATEGORY_TECHNOLOGY, 'technology'),
#     (CATEGORY_HEALTH, 'health'),
#     (CATEGORY_SCIENCE, 'science'),
#     (CATEGORY_OTHER, 'other')
# )

class Topic(models.Model):
	CATEGORY_POLITICS = 0
	CATEGORY_SPORTS = 1
	CATEGORY_BUSINESS = 2
	CATEGORY_ENTERTAINMENT = 3
	CATEGORY_TECHNOLOGY = 4
	CATEGORY_HEALTH = 5
	CATEGORY_SCIENCE = 6
	CATEGORY_OTHER = 7
	CATEGORY_CHOICES = (
	    (CATEGORY_POLITICS, 'politics'),
	    (CATEGORY_SPORTS, 'sports'),
	    (CATEGORY_BUSINESS, 'business'),
	    (CATEGORY_ENTERTAINMENT, 'entertainent'),
	    (CATEGORY_TECHNOLOGY, 'technology'),
	    (CATEGORY_HEALTH, 'health'),
	    (CATEGORY_SCIENCE, 'science'),
    	(CATEGORY_OTHER, 'other')
	)

	topic_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	topic_name = models.CharField(max_length=50)
	category_name = models.SmallIntegerField(choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
