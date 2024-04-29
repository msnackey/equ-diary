from collections import defaultdict
from datetime import datetime
from itertools import chain

from django.db import models
from django.db.models import Q
from django.urls import reverse

from accounts.models import User
from calendarapp.models import Event, ExerciseCategory


class ExerciseManager(models.Manager):
    """Exercise manager"""

    def get_all_exercises(self, user):
        """Gets all exercises from the currently signed in user."""
        events = Event.objects.get_all_events(user=user)
        exercises = list(
            chain.from_iterable(
                self.get_exercises_of_event(event)
                for event in events
                if self.get_exercises_of_event(event) is not None
            )
        )
        return exercises

    def group_exercises(self, user):
        """Groups all exercises from the currently signed in user."""
        exercises = self.get_all_exercises(user=user)
        exercise_groups = defaultdict(list)

        for exercise in exercises:
            exercise_groups[exercise.category].append(exercise)

        return dict(exercise_groups)

    def get_exercises_of_event(self, event):
        """Gets all exercises belonging to an event."""
        exercises = Exercise.objects.filter(event=event)
        if exercises:
            return exercises


class Exercise(models.Model):
    """Exercise model"""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="exercises")
    category = models.ForeignKey(
        ExerciseCategory, on_delete=models.CASCADE, related_name="exercises", null=True
    )
    reps = models.PositiveIntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)

    objects = ExerciseManager()

    def __str__(self):
        return str(self.category)
