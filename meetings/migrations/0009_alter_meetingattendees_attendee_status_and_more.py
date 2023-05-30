# Generated by Django 4.2 on 2023-04-23 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0008_alter_meeting_current_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingattendees',
            name='attendee_status',
            field=models.CharField(blank=True, choices=[('PERSONAL', 'personal'), ('GROUPY', 'groupy'), ('ORGANIZATIONAL', 'organizational'), ('OLM', 'online meeting(friendly)')], default='PERSONAL', max_length=20),
        ),
        migrations.AlterField(
            model_name='meetingattendees',
            name='attendee_status_date',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='meetingattendees',
            name='attendee_status_time',
            field=models.TimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='meetingattendees',
            name='attending',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='meetingattendees',
            name='meeting',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='meetings.meeting'),
        ),
        migrations.AlterField(
            model_name='meetingattendees',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to=settings.AUTH_USER_MODEL),
        ),
    ]
