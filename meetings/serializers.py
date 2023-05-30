from rest_framework import serializers 
from g_auth.serializers import GUserSerializer
from meetings.models import (
    Meeting,
    MeetingResource,
    MeetingAttendees
)

class MeetingResourceSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = MeetingResource
        fields = ('id', 'meeting', 'file')

class MeetingSerializer(serializers.ModelSerializer):
    user = GUserSerializer(read_only=True)
    agenda = serializers.CharField()
    purpose = serializers.CharField()
    start_time = serializers.TimeField()
    start_date = serializers.DateField()
    attendants = serializers.IntegerField()
    resources = MeetingResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Meeting 
        fields = '__all__'
        depth = 1
        
    def create(self, validated_data):
        user = validated_data.pop('user')
        meeting = Meeting.objects.create(**validated_data)
        meeting.host = user
        meeting.save()
        return meeting
    
    def update(self, instance, validated_data):
        instance.agenda = validated_data.get('agenda', instance.agenda)
        instance.purpose = validated_data.get('purpose', instance.purpose)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.description = validated_data.get('description', instance.description)
        instance.attendants = validated_data.get('attendants', instance.attendants)
        instance.save()
        return instance

class MeetingAttendeeSerializer(serializers.ModelSerializer):
    user = GUserSerializer()
    meeting = MeetingSerializer()
    attendee_status = serializers.CharField()
    attendee_status_date = serializers.DateField()
    attendee_status_time = serializers.TimeField()
    attending = serializers.BooleanField(read_only=True)

    class Meta:
        model = MeetingAttendees
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return MeetingAttendees.objects.create(**validated_data)   

    def update(self, instance, validated_data):
        instance.attendee_status = validated_data.get('attendee_status', instance.attendee_status)
        instance.attendee_status_date = validated_data.get('attendee_status_date', instance.attendee_status_date)
        instance.attendee_status_time = validated_data.get('attendee_status_time', instance.attendee_status_time)
        instance.attending = validated_data.get('attending', instance.attending)
        instance.save()
        return instance

