# Generated by Django 4.2 on 2023-04-19 14:27

from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meetings', '0005_alter_meeting_agenda_alter_meeting_desciption_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='desciption',
            field=models.TextField(default='description'),
        ),
        migrations.AlterField(
            model_name='meetingresource',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='meetingresources/'), upload_to=''),
        ),
        migrations.CreateModel(
            name='MeetingAttendees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendee_status', models.CharField(choices=[('PERSONAL', 'personal'), ('GROUPY', 'groupy'), ('ORGANIZATIONAL', 'organizational'), ('OLM', 'online meeting(friendly)')], default='PERSONAL', max_length=20)),
                ('attendee_status_date', models.DateField()),
                ('attendee_status_time', models.TimeField()),
                ('attending', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to='meetings.meeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendees', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
