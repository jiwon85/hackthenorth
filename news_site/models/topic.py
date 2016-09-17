from django.db import models

class Topic(models.Model):
	topic_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
	topic_name = models.CharField(max_length=50)
	category_name = CategoryEnum(choices=CATEGORY_CHOICES)

class CategoryEnum(models.Field):

    def __init__(self, *args, **kwargs):
        super(CategoryEnum, self).__init__(*args, **kwargs)
        if not self.choices:
            raise AttributeError('EnumField requires `choices` attribute.')

    def db_type(self):
        return "enum(%s)" % ','.join("'%s'" % k for (k, _) in self.choices)

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