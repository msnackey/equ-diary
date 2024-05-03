from django.urls import path

from . import views

app_name = "calendarapp"


urlpatterns = [
    path("", views.CalendarView.as_view(), name="calendar"),
    path("evaluation/", views.OverviewView.as_view(), name="overview"),
    path("event/new/", views.EventModalCreateView.as_view(), name="event"),
    path(
        "event/new/<str:date>/",
        views.EventModalCreateView.as_view(),
        name="event_create",
    ),
    path(
        "event/details/<int:pk>/",
        views.EventDetailsModalUpdateView.as_view(),
        name="event_details",
    ),
    path(
        "event/edit/<int:pk>/",
        views.EventEditModalUpdateView.as_view(),
        name="event_edit",
    ),
    path(
        "event/post_edit/<int:pk>/",
        views.EventPostEditModalUpdateView.as_view(),
        name="event_post_edit",
    ),
    path(
        "event/remove/<int:pk>/",
        views.EventDeleteModalUpdateView.as_view(),
        name="event_delete",
    ),
    path(
        "eventcategory/new/",
        views.EventCategoryCreateView.as_view(),
        name="eventcategory_create",
    ),
    path("all-events-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "upcoming-events-list/",
        views.UpcomingEventsListView.as_view(),
        name="upcoming_events",
    ),
    path("exercises-list/", views.AllExercisesListView.as_view(), name="exercises"),
    path("exercise/new/", views.ExerciseModalCreateView.as_view(), name="exercise"),
]
