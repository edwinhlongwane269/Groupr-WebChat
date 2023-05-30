from django.db import models
from django.conf import settings
from django_cryptography.fields import encrypt
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Tutorial(models.Model):
    tuitor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='user')
    lesson = models.CharField(max_length=1000, blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField('Student', blank=True, related_name="attendees+")
   
    def __str__(self):
        return f"Tuitorial by {self.tuitor.username} on lesson {self.lesson}"

class Student(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)

    def __str__(self):
        return f"Students attending {self.tutorial.lesson}"

class TutorialResource(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    file = models.FileField(storage=FileSystemStorage(location="tutorialresources/"))

    def __str__(self):
        return f"Resource for {self.tutorial}"