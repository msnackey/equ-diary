from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from calendarapp.models import Event


class CalendarView(LoginRequiredMixin, generic.View):
    login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        for event in events:
            event_list.append(
                {
                    "event_pk": event.pk,
                    "url_details": reverse('calendarapp:event_details', kwargs={'pk': event.pk}),
                    "url_edit": reverse('calendarapp:event_edit', kwargs={'pk': event.pk}),
                    "url_delete": reverse('calendarapp:event_delete', kwargs={'pk': event.pk}),
                    "parent_category": event.category.parent_category.name,
                    "title": event.title,
                    "description": event.description,
                    "allDay": int(event.all_day),
                    "start": event.start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                    "planned_exertion": event.planned_exertion, 
                }
            )
        context = {"events": event_list, "events_month": events_month}
        return render(request, self.template_name, context)
