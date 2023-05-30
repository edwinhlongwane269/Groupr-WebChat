from g_auth.serializers import GUserSerializer
from rest_framework import serializers
from groups.models import (
    Group,
    GroupMessage,
    GroupAttendee
)

class GroupmessageSerializer(serializers.ModelSerializer):
    user = GUserSerializer()
    message = serializers.CharField()
    created_at_formatted = serializers.SerializerMethodField()


    class Meta:
        model = GroupMessage
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj:GroupMessage):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")   


class GroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    group_description = serializers.CharField(required=True, allow_blank=False)
    max_attendees = serializers.IntegerField(read_only=True)
    last_message = serializers.SerializerMethodField()
    messages = GroupmessageSerializer(many=True, read_only=True)
    current_users = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'
        depth = 1 
        read_only_fields = ["messages", "last_message"]

    def create(self, validated_data):
        """
        Create and return a new `Group` instance, given the validated data.
        """    
        return Group.objects.create(**validated_data)    

    def update(self, instance, validated_data):
        """
        Update and return an existing `Group` instance given the validated data.
        """
        instance.group_name = validated_data.get('group_name', instance.group_name)
        instance.group_description = validated_data.get('group_description', instance.group_description)
        instance.max_attendees = validated_data.get('max_attendees', instance.max_attendees)
        instance.save()
        return instance    

    def get_last_message(self, obj:Group):
        pass 

    def get_current_users(self, obj: Group):
        return obj.current_users
       

# class GroupAttendeeSerializer(serializers.ModelSerializer):
#     user = GUserSerializer()
#     group = GroupSerializer()

#     class Meta:
#         model = GroupAttendee
#         fields = '__all__'
#         depth = 1 

#     def create(self, validated_data):
#         return GroupAttendee.objects.create(**validated_data)
           
class GroupAttendeeSerializer(serializers.ModelSerializer):
    user = GUserSerializer()
    group = GroupSerializer()
    is_attending = serializers.BooleanField(default=False)
    created_at_formatted = serializers.SerializerMethodField()


    class Meta:
        model = GroupAttendee
        exclude = []
        depth = 1

    def get_created_at_formatted(self, obj:GroupAttendee):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")   
