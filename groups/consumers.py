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
from groups.models import Group, GroupMessage
from groups.serializers import GroupmessageSerializer, GroupSerializer
from g_auth.serializers import GUserSerializer

# Acts as a viewset for the rest framework serializer, 
# returns a response through a websocket consumer
# allowing us to map,the users in the group more efficiently.

class GroupConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    lookup_field = "pk"

    # The websocket consumer uses asynchronus functions 
    async def disconnect(self, code):
        if hasattr(self, "group_subscribe"):
            await self.remove_user_from_group(self.group_subscribe)
            await self.notify_users()
        await super().disconnect(code)    

    # User functionality actions 
    @action()   
    async def join_group(self, pk, **kwargs):
        self.group_subscribe = pk
        await self.add_user_to_group(pk)
        await self.notify_users()

    @action()
    async def leave_group(self, pk, **kwargs):
        await self.remove_user_from_group(pk)

    @action()
    async def create_message(self, message, **kwargs):
        group: Group = await self.get_group(pk=self.group_subscribe)
        await database_sync_to_async(GroupMessage.objects.create(
            group=group,
            user=self.scope["user"],
            message=message,
        ))
    
    @action()
    async def subscibe_to_message_in_group(self, pk, request_id, **kwargs):
        await self.message_activity.subscribe(group=pk, request_id=request_id)

    @model_observer(GroupMessage)
    async def message_activity(self, message, observer=None, subscribing_request_ids=[], **kwargs):
        """
        This is evaluated once for each subscribed consumer
        The result of `@message_activity.serializer` is provided here as the message
        """    
        # Since wwe provide the request_id when subscribing we 
        # can just loop over them here
        for request_id in subscribing_request_ids:
            # The consumer is responsible for the request_id
            message_body = dict(request_id=request_id)
            message_body.update(message)
            await self.send_json(message_body)

    @message_activity.groups_for_signal
    def message_activity(self, instance: GroupMessage, **kwargs):
        yield 'group__{instance.group_id}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, group=None, **kwargs):
        if group is None:
            yield f'group__{group}'   

    @message_activity.serializer
    def message_activity(self, instance:GroupMessage, action, **kwargs):
        """
        This is evaluated before the update is sent
        out to all the subscribing consumers.
        """                 
        return dict(data=GroupmessageSerializer(instance).data, action=action.value, pk=instance.pk)
    
    async def notify_users(self):
        group: Group = await self.get_group(self.group_subscribe)
        for group_id in self.groups:
            
            await self.channel_layer.send(
                group_id,
                {
                    'type': 'update_users',
                    'usuarios': await self.current_users(group)
                }
            ) 

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'usuarios': event["usuarios"]}))

    @database_sync_to_async
    def get_group(self, pk: int) -> Group:
        return Group.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, group: Group):
        return [GUserSerializer(user).data for user in group.current_users.all()]

    @database_sync_to_async
    def remove_user_from_group(self, group):
        user:get_user_model() = self.scope["user"]
        user.current_groups.remove(group)

    @database_sync_to_async
    def add_user_to_group(self, pk):
        user: get_user_model() = self.scope["user"]
        if not user.current_groups.filter(pk=self.group_subscribe).exists():
            user.current_groups.add(Group.objects.get(pk=pk))                