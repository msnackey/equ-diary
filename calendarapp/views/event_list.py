from django.views.generic import ListView

from calendarapp.models import Event


class AllEventsListView(ListView):
    """All events list view."""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)


class UpcomingEventsListView(ListView):
    """Upcoming events list view."""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_upcoming_events(user=self.request.user)
