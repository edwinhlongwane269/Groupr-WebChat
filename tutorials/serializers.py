from rest_framework import serializers 
from g_auth.serializers import GUserSerializer
from tutorials.models import (
    Tutorial,
    TutorialResource,
    Student
)

class TutorialResourcesSerializer(serializers.ModelSerializer):
    file = serializers.FileField()

    class Meta:
        model = TutorialResource
        fields = ('id', 'file', 'tutorial')

class TutorialSerializer(serializers.ModelSerializer):
    tutor = GUserSerializer()
    lesson = serializers.CharField()
    resources = TutorialResourcesSerializer(many=True)

    class Meta:
        model = Tutorial
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        tutor = validated_data.pop('user')
        tutorial = Tutorial.objects.create(**validated_data)
        tutorial.tuitor = tutor
        tutorial.save()
        return tutorial

    def update(self, instance, validated_data):
        instance.lesson = validated_data.get('lesson')
        instance.description = validated_data.get('description') 
        instance.save()
        return instance  

class StudentSerializer(serializers.ModelSerializer):
    user = GUserSerializer()
    tutorial = TutorialSerializer()

    class Meta:
        model = Student
        fields = '__all__'
        depth = 1

    def create(self, validated_data):
        return Student.objects.create(**validated_data)
    
    