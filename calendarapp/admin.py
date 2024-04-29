from django.contrib import admin

from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    model = models.Event
    list_display = [
        "id",
        "title",
        "user",
        "category",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["category", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    model = models.EventCategory
    list_display = [
        "id",
        "name",
        "parent_category",
    ]


@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    model = models.Exercise


@admin.register(models.ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    model = models.ExerciseCategory
