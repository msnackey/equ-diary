from datetime import datetime

from bootstrap_modal_forms import generic as bsmfg
from django.urls import reverse_lazy
from django.views.generic import ListView

from calendarapp.forms import ExerciseModalForm
from calendarapp.models import Exercise


class AllExercisesListView(ListView):
    """All exercises list view."""

    template_name = "calendarapp/exercises.html"
    model = Exercise

    def get_queryset(self):
        return Exercise.objects.group_exercises(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rand"] = int(datetime.now().strftime("%Y%m%d"))
        context["excluded_exercises"] = ""
        return context


class ExerciseModalCreateView(bsmfg.BSModalCreateView):
    """Event create view with Bootstrap Modal CreateView."""

    template_name = "calendarapp/exercise.html"
    form_class = ExerciseModalForm
    success_url = reverse_lazy("calendarapp:exercises")

    def form_valid(self, form):
        """Adds additional checks to determine the form validity."""
        self.object = form.save(commit=False)
        self.object.user = (
            self.request.user
        )  # Gets the user from the request and sets it as the object.user

        return super().form_valid(form)
