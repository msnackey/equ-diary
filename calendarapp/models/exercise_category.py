from django.db import models


class ExerciseCategory(models.Model):
    """ExerciseCategory model"""

    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
