# Generated by Django 4.2 on 2023-04-23 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0007_meeting_current_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='current_users',
            field=models.ManyToManyField(blank=True, related_name='attendee+', to='meetings.meetingattendees'),
        ),
    ]
