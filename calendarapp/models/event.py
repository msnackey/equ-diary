from datetime import datetime

from django.db import models
from django.db.models import Q
from django.urls import reverse

from accounts.models import User
from calendarapp.models import EventAbstract, EventCategory


class EventManager(models.Manager):
    """Event manager"""

    def get_all_events(self, user):
        """Gets all non-deleted events from the currently signed in user."""
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_upcoming_events(self, user):
        """Gets the upcoming events from the currently signed in user."""
        upcoming_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_datetime__gte=datetime.now(),
        ).order_by("start_datetime")
        return upcoming_events

    def get_post_events(self, user):
        """Gets all post events from the currently signed in user."""
        post_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            is_post=True,
        ).order_by("-start_datetime")
        return post_events

    def get_last_five_events(self, user, category):
        """Gets the last five events from the currently signed in user where
        negative feedback (post_fb_neg) has been entered and the category equals the category parameter.
        """
        last_five_events = (
            Event.objects.filter(
                user=user,
                is_active=True,
                is_deleted=False,
                end_datetime__lte=datetime.now(),
                category=category,
            )
            .exclude(
                post_fb_neg="",
            )
            .order_by("-start_datetime")[:5]
        )
        return last_five_events


class Event(EventAbstract):
    """Event model"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    category = models.ForeignKey(
        EventCategory, on_delete=models.CASCADE, related_name="events"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    all_day = models.BooleanField(default=False)
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    planned_exertion = models.PositiveSmallIntegerField(blank=True, null=True)
    # 'post_' fields are updated by the user after an event has occurred
    post_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    post_exertion = models.PositiveSmallIntegerField(blank=True, null=True)
    post_fb_neg = models.TextField(blank=True)
    post_fb_pos = models.TextField(blank=True)
    post_comments = models.TextField(blank=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse("calendarapp:event-details", args=(self.id,))
