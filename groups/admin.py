from django.contrib import admin
from groups.models import Group, GroupAttendee, GroupMessage
# Register your models here.

class GroupAttendeeInline(admin.StackedInline):
    model = Group
    can_delete = True
    max_num = 10
    min_num=1
    verbose_name_plural = 'Attendants'

class GroupMessagesInline(admin.StackedInline):
    model = GroupMessage
    can_delete = True
    min_num =1
    max_num = 10
    verbose_name_plural = 'Messages'

class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = (GroupMessagesInline,)

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupAttendee)
admin.site.register(GroupMessage)