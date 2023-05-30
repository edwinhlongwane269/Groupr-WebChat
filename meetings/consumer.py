import json 
from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils.timezone import now
from django.conf import settings
from typing import Generator
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer, AsyncAPIConsumer
from djangochannelsrestframework.observer.generics import (
    ObserverModelInstanceMixin,
    action
)
from djangochannelsrestframework.observer import model_observer
from django.contrib.auth import get_user_model
from g_auth.serializers import GUserSerializer
from meetings.models import (
    Meeting,
    MeetingResource,
    MeetingAttendees
)
from meetings.serializers import (
    MeetingAttendeeSerializer,
    MeetingResourceSerializer,
    MeetingSerializer,
)

class MeetingConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    lookup_field = "pk"

    async def disconnect(self, code):
        if hasattr(self, "meeting_subscribe"):
            await self.remove_attendee_from_meeting(self.meeting_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_meeting(self, pk, **kwargs):
        self.meeting_subscribe = pk
        await self.grant_user_access_to_meeting(pk) 
        await self.notify_users()

    @action()
    async def leave_meeting(self, pk, **kwargs):
        await self.remove_attendee_from_meeting(pk)
        await self.notify_users()
    
    async def notify_users(self):
        meeting: Meeting = await self.get_meeting(self.meeting_subscribe)
        for group in self.groups:
            await self.channel_layer.send(
                group,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(group)
                }
            ) 
    
    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_meeting(self, pk: int) -> Meeting:
        return Meeting.objects.get(pk=pk)
    
    @database_sync_to_async
    def current_users(self, group: Meeting):
        return [GUserSerializer(user).data for user in group.current_users.all()]
    
    @database_sync_to_async
    def remove_attendee_from_meeting(self, group):
        user:get_user_model() = self.scope["user"]
        meetingattendee = MeetingAttendees.objects.delete(
            user=user,
        )  
        meetingattendee.save()
        user.current_meetings.remove(group)
    
    @database_sync_to_async
    def grant_user_access_to_meeting(self, pk):
        user:get_user_model() = self.scope["user"]
        if user != MeetingAttendees.objects.filter(user=user):
            if not user.current_meetings.filter(pk=self.meeting_subscribe).exists():
                user.current_meetings.add(self.get_meeting(pk))
        else:
            raise SystemExit()
        
