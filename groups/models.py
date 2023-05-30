from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt
# Create your models here.

class Group(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=100, blank=True, null=True, default='')
    group_description = models.TextField(blank=True, null=True, default='')
    max_attendees = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    current_users = models.ManyToManyField('GroupAttendee', related_name="attendants-rooms+", blank=True)

    def __str__(self):
        return f"Group({self.group_name} {self.user.username})"
    
    def total_attendees(self):
        return self.current_users.count()

class GroupMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messenger+")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.TextField(max_length=5000, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from({self.user.username} {self.message})"
    
class GroupAttendee(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="attendee+")
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_attending = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.id} {self.user.username}"