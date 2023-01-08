from django.db import models


class EventCategoryManager(models.Manager):
    """EventCategory manager"""
    
    def get_parent_categories(self):
        """Gets all parent categories. These are defined as itself having a parent category."""
        parent_categories = EventCategory.objects.filter(parent_category__isnull=True)
        return parent_categories

    def get_categories(self):
        """Gets all categores. These are defined as having a parent category."""
        categories = EventCategory.objects.exclude(parent_category__isnull=True)
        return categories


class EventCategory(models.Model):
    """EventCategory model"""

    name = models.CharField(max_length=256, unique=True)
    parent_category = models.ForeignKey(
        'self', related_name='categories',
        on_delete=models.SET_NULL, blank=True, null=True,
    )

    objects = EventCategoryManager()

    def __str__(self):
        return self.name
