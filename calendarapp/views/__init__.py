from .calendar_views import CalendarView
from .event_list import AllEventsListView, UpcomingEventsListView
from .event_views import (
    EventDeleteModalUpdateView,
    EventDetailsModalUpdateView,
    EventEditModalUpdateView,
    EventModalCreateView,
    EventPostEditModalUpdateView,
)
from .exercises_views import AllExercisesListView, ExerciseModalCreateView
from .other_views import EventCategoryCreateView, OverviewView

__all__ = [
    AllEventsListView,
    UpcomingEventsListView,
    CalendarView,
    EventModalCreateView,
    EventDetailsModalUpdateView,
    EventEditModalUpdateView,
    EventDeleteModalUpdateView,
    OverviewView,
    EventPostEditModalUpdateView,
    EventCategoryCreateView,
    AllExercisesListView,
    ExerciseModalCreateView,
]
