# Generated by Django 3.2.14 on 2023-01-01 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarapp', '0004_auto_20221229_0754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='EventMember',
        ),
    ]