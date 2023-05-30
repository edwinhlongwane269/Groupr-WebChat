from django.db import models
from django.conf import settings
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage
from django_cryptography.fields import encrypt
# Create your models here.

class Meeting(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Host+")
    agenda = models.CharField(max_length=2000, blank=True, null=True)
    PURPOSE = (
        ('PERSONAL', 'personal'),
        ('GROUPY', 'groupy'),
        ('ORGANIZATIONAL', 'organizational'),
        ('OLM', 'online meeting(friendly)')
    )
    purpose = models.CharField(max_length=20, choices=PURPOSE, default='PERSONAL')
    start_time = models.TimeField(auto_created=False)
    start_date = models.DateField(auto_created=False)
    desciption = models.TextField(default="description")
    attendants = models.IntegerField(default=0)
    current_users = models.ManyToManyField('MeetingAttendees', related_name="attendee+", blank=True)

    def __str__(self):
        return f"Schuduled meeting: {self.agenda} hosted by :{self.host.username}"

class MeetingAttendees(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="attendees", blank=True,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendees", blank=True,)
    attendee_status = models.CharField(max_length=20, choices=Meeting.PURPOSE, default='PERSONAL', blank=True,)
    attendee_status_date = models.DateField(auto_created=False, blank=True,)
    attendee_status_time = models.TimeField(auto_created=False, blank=True,)
    attending = models.BooleanField(default=False, blank=True,)

    def __str__(self):
        return f"{self.user.username}"
    
   
class MeetingResource(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name="resources")
    file = models.FileField(storage=FileSystemStorage(location='meetingresources/'))

    def __str__(self):
        return f"Resources for {self.meeting.agenda} : Meeting"
