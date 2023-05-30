from django.contrib import admin
from meetings.models import (
    Meeting,
    MeetingResource,
    MeetingAttendees
)
# Register your models here.
class ResourceInline(admin.StackedInline):
    model = MeetingResource
    can_delete = True
    min_num = 1
    max_num = 10
    verbose_name_plural = 'Meeting Resources'

class AttendeeInline(admin.StackedInline):
    model = MeetingAttendees
    can_delete = True
    min_num = 1
    max_num = 10
    verbose_name_plural = 'Meeting Attendants'

class MeetingAdmin(admin.ModelAdmin):
    model = Meeting
    inlines = (ResourceInline, AttendeeInline,)

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(MeetingResource)
admin.site.register(MeetingAttendees)