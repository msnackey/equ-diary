from django.views.generic import ListView

from datetime import datetime

from calendarapp.models import Event


class AllEventsListView(ListView):
    """All events list view."""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand"] = int(datetime.now().strftime("%Y%m%d"))
        return context


class UpcomingEventsListView(ListView):
    """Upcoming events list view."""

    template_name = "calendarapp/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_upcoming_events(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand"] = int(datetime.now().strftime("%Y%m%d"))
        return context
