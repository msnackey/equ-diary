from django.db import models


class EventCategoryManager(models.Manager):
    def get_parent_categories(self):
        parent_categories = EventCategory.objects.filter(parent_category__isnull=True)
        return parent_categories

    def get_categories(self):
        categories = EventCategory.objects.exclude(parent_category__isnull=True)
        return categories


class EventCategory(models.Model):
    name = models.CharField(max_length=256, unique=True)
    parent_category = models.ForeignKey(
        'self', related_name='sub_categories',
        on_delete=models.SET_NULL, blank=True, null=True,
    )

    objects = EventCategoryManager()

    def __str__(self):
        return self.name
