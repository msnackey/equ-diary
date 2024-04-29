from .calendar_views import CalendarView
from .event_list import AllEventsListView, UpcomingEventsListView
from .event_views import (
    EventDeleteModalUpdateView,
    EventDetailsModalUpdateView,
    EventEditModalUpdateView,
    EventModalCreateView,
    EventPostEditModalUpdateView,
)
from .exercises_list import AllExercisesListView
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
]
