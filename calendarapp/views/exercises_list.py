from django.views.generic import ListView

from datetime import datetime

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
        context["excluded_exercises"] = "Ex3"
        return context
