from .calendar_views import CalendarView
from .event_views import (EventModalCreateView, EventDetailsModalUpdateView, EventEditModalUpdateView,
                          EventDeleteModalUpdateView, EventPostEditModalUpdateView)
from .event_list import AllEventsListView, RunningEventsListView
from .other_views import OverviewView, EventCategoryCreateView


__all__ = [
    AllEventsListView,
    RunningEventsListView,
    CalendarView,
    EventModalCreateView,
    EventDetailsModalUpdateView,
    EventEditModalUpdateView,
    EventDeleteModalUpdateView,
    OverviewView,
    EventPostEditModalUpdateView,
    EventCategoryCreateView,
]
