# Generated by Django 4.2 on 2023-04-22 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0006_alter_meeting_desciption_alter_meetingresource_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='current_users',
            field=models.ManyToManyField(related_name='attendee+', to='meetings.meetingattendees'),
        ),
    ]