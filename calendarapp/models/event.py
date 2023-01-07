from datetime import datetime
from django.db import models
from django.urls import reverse
from django.db.models import Q

from calendarapp.models import EventAbstract, EventCategory
from accounts.models import User


class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_datetime__gte=datetime.now(),
        ).order_by("start_datetime")[:6]
        return running_events

    def get_past_work_events(self, user):
        past_events = Event.objects.filter(
            Q(user=user),
            Q(is_active=True),
            Q(is_deleted=False),
            Q(end_datetime__lte=datetime.now()),
            ~Q(post_rating__isnull=True) | ~Q(post_exertion__isnull=True) | ~Q(post_fb_neg="") | ~Q(post_fb_pos="") | ~Q(post_comments=""),
        ).order_by("-start_datetime")
        return past_events

    def get_last_five_events(self, user, category):
        last_five_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_datetime__lte=datetime.now(),
            category=category,
        ).exclude(
            post_fb_neg="",
        ).order_by("-start_datetime")[:5]
        return last_five_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name="tests")
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
    post_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    post_exertion = models.PositiveSmallIntegerField(blank=True, null=True)
    post_fb_neg = models.TextField(blank=True)
    post_fb_pos = models.TextField(blank=True)
    post_comments = models.TextField(blank=True)

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("calendarapp:event-details", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-details", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
