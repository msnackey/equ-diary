# Generated by Django 4.1.5 on 2024-04-27 12:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("calendarapp", "0019_remove_exercise_category_remove_exercise_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="exercise",
            name="duration",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="exercise",
            name="reps",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
