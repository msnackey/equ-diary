from django.views import generic
from bootstrap_modal_forms import generic as bsmfg
from datetime import timedelta, datetime, date, time
import calendar
from django.urls import reverse_lazy
from django.core import serializers

from calendarapp.models import Event, EventCategory
from calendarapp.forms import EventModalForm, EventDetailsModalForm


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


class EventModalCreateView(bsmfg.BSModalCreateView):
    template_name = 'calendarapp/event.html'
    form_class = EventModalForm
    success_url = reverse_lazy('calendarapp:calendar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        parent_categories = EventCategory.objects.get_parent_categories()
        categories = serializers.serialize("json", EventCategory.objects.get_categories())

        context.update({'parent_categories': parent_categories, 'categories': categories,})

        return context

    def get_form_kwargs(self):
        """Adds the <date> from the form url as form kwarg"""
        kwargs = super(EventModalCreateView, self).get_form_kwargs()
        # self.kwargs holds all the kwargs of the view
        date = datetime.strptime(self.kwargs['date'], "%Y-%m-%d").date()
        kwargs.update({'date': date})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        if self.object.start_time is None:
            self.object.all_day = True
            self.object.start_time = time(0, 0, 0, 0)
            self.object.end_time = time(0, 0, 0, 0)

        if self.object.end_date is None:
            self.object.end_date = self.object.start_date

        self.object.start_datetime = datetime.combine(self.object.start_date, self.object.start_time)
        self.object.end_datetime = datetime.combine(self.object.end_date, self.object.end_time)

        return super().form_valid(form)


class EventDetailsModalUpdateView(bsmfg.BSModalUpdateView):
    model = Event
    template_name = 'calendarapp/event_details.html'
    form_class = EventDetailsModalForm
    success_url = reverse_lazy('calendarapp:calendar')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_post = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()

        last_five_events = Event.objects.get_last_five_events(user=self.request.user, category=self.object.category)

        context.update({'now': now, 'last_events': last_five_events})

        return context


class EventPostEditModalUpdateView(bsmfg.BSModalUpdateView):
    model = Event
    template_name = 'calendarapp/event_post_edit.html'
    form_class = EventDetailsModalForm
    success_url = reverse_lazy('calendarapp:calendar')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_post = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()
        context['now'] = now

        return context


class EventEditModalUpdateView(bsmfg.BSModalUpdateView):
    model = Event
    template_name = 'calendarapp/event_edit.html'
    form_class = EventModalForm
    success_url = reverse_lazy('calendarapp:calendar')

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.start_time is None:
            self.object.all_day = True
            self.object.start_time = time(0, 0, 0, 0)
            self.object.end_time = time(0, 0, 0, 0)

        if self.object.end_date is None:
            self.object.end_date = self.object.start_date

        self.object.start_datetime = datetime.combine(self.object.start_date, self.object.start_time)
        self.object.end_datetime = datetime.combine(self.object.end_date, self.object.end_time)

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()
        
        parent_categories = EventCategory.objects.get_parent_categories()
        categories = serializers.serialize("json", EventCategory.objects.get_categories())

        context.update({'now': now, 'parent_categories': parent_categories, 'categories': categories,})

        return context


class EventDeleteModalUpdateView(generic.UpdateView):
    model = Event
    template_name = 'calendarapp/event_delete.html'
    fields = ['is_deleted']
    success_url = reverse_lazy('calendarapp:calendar')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_deleted = True
        return super().form_valid(form)
