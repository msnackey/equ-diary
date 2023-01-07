# Generated by Django 3.2.14 on 2023-01-02 10:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0007_event_all_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_day',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='start_day',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]