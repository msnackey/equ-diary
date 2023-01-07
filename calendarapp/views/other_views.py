from django.views.generic import View, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from datetime import timedelta, datetime, date
import calendar

from calendarapp.models import Event, EventCategory
from calendarapp.forms import EventCategoryForm


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class OverviewView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/overview.html"

    def get(self, request, *args, **kwargs):
        past_events = Event.objects.get_past_work_events(user=request.user)
        context = {
            "past_events": past_events,
        }
        return render(request, self.template_name, context)


class EventCategoryCreateView(CreateView):
    template_name = "calendarapp/eventcategory_create.html"
    form_class = EventCategoryForm
    success_url = reverse_lazy('calendarapp:calendar')
