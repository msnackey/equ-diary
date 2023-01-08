from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from calendarapp.models import Event


class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        events = Event.objects.get_all_events(user=request.user)
        upcoming_events = Event.objects.get_upcoming_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "upcoming_events": upcoming_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
