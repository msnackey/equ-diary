from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime

from calendarapp.models import Event


class CalendarView(LoginRequiredMixin, generic.View):
    """The main calendar view."""

    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"

    def get(self, request, *args, **kwargs):
        """Gets all events from the currently signed in user to display in the FullCalendar."""
        events = Event.objects.get_all_events(user=request.user)
        event_list = []
        for event in events:
            event_list.append(
                {
                    "event_pk": event.pk,
                    # url's are added so they can be used in Bootstrap Modal Forms from the calendar template 
                    "url_details": reverse('calendarapp:event_details', kwargs={'pk': event.pk}),
                    "url_edit": reverse('calendarapp:event_edit', kwargs={'pk': event.pk}),
                    "url_delete": reverse('calendarapp:event_delete', kwargs={'pk': event.pk}),
                    "parent_category": event.category.parent_category.name, # used for adding CSS classes
                    "title": event.title,
                    "description": event.description,
                    "allDay": int(event.all_day), # uses int() so that the boolean gets translated to JS boolean (0/1)
                    "start": event.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    "planned_exertion": event.planned_exertion, # used for adding CSS classes
                }
            )
        rand = int(datetime.now().strftime("%Y%m%d"))
        context = {"events": event_list, "rand": rand}
        return render(request, self.template_name, context)
