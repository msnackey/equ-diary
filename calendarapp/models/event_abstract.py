from django.db import models


class EventAbstract(models.Model):
    """Event abstract model. Adds meta fields to events."""

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_post = models.BooleanField(
        default=False
    )  # 'is_post' is true when an event has been updated with feedback after occurring

    class Meta:
        abstract = True
        # ordering = ["-created_at"]
