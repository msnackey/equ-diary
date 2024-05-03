import calendar
from datetime import date, datetime, time, timedelta

from bootstrap_modal_forms import generic as bsmfg
from django.core import serializers
from django.urls import reverse_lazy
from django.views import generic

from calendarapp.forms import EventDetailsModalForm, EventModalForm
from calendarapp.models import Event, EventCategory


class EventModalCreateView(bsmfg.BSModalCreateView):
    """Event create view with Bootstrap Modal CreateView."""

    template_name = "calendarapp/event.html"
    form_class = EventModalForm
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        """Adds additional checks to determine the form validity."""
        self.object = form.save(commit=False)
        self.object.user = (
            self.request.user
        )  # Gets the user from the request and sets it as the object.user

        # If no start_time is inputted, derives that the event is an allDay event
        # and fills the missing fields with the appopriate data
        if self.object.start_time is None:
            self.object.all_day = True
            self.object.start_time = time(0, 0, 0, 0)
            self.object.end_time = time(0, 0, 0, 0)

        # If no end_date is inputted, derives that the event ends on the start_date
        # and fills the end_date with the inputted start_date
        if self.object.end_date is None:
            self.object.end_date = self.object.start_date

        # Combines the inputted date and time to datetimes for start and end
        self.object.start_datetime = datetime.combine(
            self.object.start_date, self.object.start_time
        )
        self.object.end_datetime = datetime.combine(
            self.object.end_date, self.object.end_time
        )

        return super().form_valid(form)

    def get_form_kwargs(self):
        """Adds the <date> from the form url to the form kwargs"""
        kwargs = super(EventModalCreateView, self).get_form_kwargs()
        # self.kwargs holds all the kwargs of the view
        date = datetime.strptime(self.kwargs["date"], "%Y-%m-%d").date()
        kwargs.update({"date": date})
        return kwargs

    def get_context_data(self, **kwargs):
        """Adds categories and parent categories to the context of the view."""
        context = super().get_context_data(**kwargs)

        parent_categories = EventCategory.objects.get_parent_categories()
        categories = serializers.serialize(
            "json", EventCategory.objects.get_categories()
        )  # serialize as json so JS can unpack it

        context.update(
            {
                "parent_categories": parent_categories,
                "categories": categories,
            }
        )

        return context


class EventEditModalUpdateView(bsmfg.BSModalUpdateView):
    """Event edit view with Bootstrap Modal UpdateView."""

    model = Event
    template_name = "calendarapp/event_edit.html"
    form_class = EventModalForm
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        """Adds additional checks to determine the form validity."""
        self.object = form.save(commit=False)

        # If no start_time is inputted, derives that the event is an allDay event
        # and fills the missing fields with the appopriate data
        if self.object.start_time is None:
            self.object.all_day = True
            self.object.start_time = time(0, 0, 0, 0)
            self.object.end_time = time(0, 0, 0, 0)

        # If no end_date is inputted, derives that the event ends on the start_date
        # and fills the end_date with the inputted start_date
        if self.object.end_date is None:
            self.object.end_date = self.object.start_date

        # Combines the inputted date and time to datetimes for start and end
        self.object.start_datetime = datetime.combine(
            self.object.start_date, self.object.start_time
        )
        self.object.end_datetime = datetime.combine(
            self.object.end_date, self.object.end_time
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds categories and parent categories to the context of the view."""
        context = super().get_context_data(**kwargs)

        now = datetime.now()

        parent_categories = EventCategory.objects.get_parent_categories()
        categories = serializers.serialize(
            "json", EventCategory.objects.get_categories()
        )  # serialize as json so JS can unpack it

        context.update(
            {
                "now": now,
                "parent_categories": parent_categories,
                "categories": categories,
            }
        )

        return context


class EventDetailsModalUpdateView(bsmfg.BSModalUpdateView):
    """Event details view with Bootstrap Modal UpdateView. Allows the user to see the details of an existing event
    but also allows them to submit feedback when the event has occurred; this requires the view to be an UpdateView.
    """

    model = Event
    template_name = "calendarapp/event_details.html"
    form_class = EventDetailsModalForm
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        """When feedback is submitted, changes the is_post value to True."""
        self.object = form.save(commit=False)
        self.object.is_post = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds additional context."""
        context = super().get_context_data(**kwargs)

        now = (
            datetime.now()
        )  # Used in templates to determine if an event is past or future

        last_five_events = Event.objects.get_last_five_events(
            user=self.request.user, category=self.object.category
        )

        context.update({"now": now, "last_events": last_five_events})

        return context


class EventPostEditModalUpdateView(bsmfg.BSModalUpdateView):
    """Event edit view with Bootstrap Modal UpdateView where the event.is_post=True. Allows the user to edit an event
    when they have already submitted feedback before."""

    model = Event
    template_name = "calendarapp/event_post_edit.html"
    form_class = EventDetailsModalForm
    success_url = reverse_lazy("calendarapp:calendar")

    def form_valid(self, form):
        """When feedback is submitted, changes the is_post value to True."""
        self.object = form.save(commit=False)
        self.object.is_post = True
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Adds additional context."""
        context = super().get_context_data(**kwargs)

        now = (
            datetime.now()
        )  # Used in templates to determine if an event is past or future
        context["now"] = now

        return context


# class EventDeleteModalUpdateView(generic.UpdateView):
#     """Event delete view with Bootstrap Modal UpdateView. Instead of a normal DeleteView, this UpdateView allows
#     the user to update the 'is_deleted' field of an event."""

#     model = Event
#     template_name = "calendarapp/event_delete.html"
#     fields = ["is_deleted"]
#     success_url = reverse_lazy("calendarapp:calendar")

#     def form_valid(self, form):
#         """When the form is submitted, changes the event field 'is_deleted' to True."""
#         self.object = form.save(commit=False)
#         # self.object.is_deleted = True
#         self.object.delete()
#         return super().form_valid(form)


class EventDeleteModalUpdateView(bsmfg.BSModalDeleteView):
    model = Event
    template_name = "calendarapp/event_delete.html"
    success_message = "Success: Event was deleted."
    success_url = reverse_lazy("calendarapp:overview")
