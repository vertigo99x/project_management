from rest_framework import serializers 
from .models import Project, Activities
from accounts.models import User
from accounts.serializers import UserSerializer



class ProjectSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Project
        fields = ['uuid', 'project_name', 'project_description', 'status', 'priority', 'assigned_to', 'assigned_to_id', 'date_created']

    def create(self, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        project = Project.objects.create(**validated_data)
        
        if assigned_to_id:
            project.assigned_to = User.objects.get(id=assigned_to_id)
            project.save()
        
        return project

    def update(self, instance, validated_data):
        assigned_to_id = validated_data.pop('assigned_to_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if assigned_to_id:
            instance.assigned_to = User.objects.get(id=assigned_to_id)
        instance.save()
        
        return instance
    
class ActivitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Activities
        fields = '__all__'
        
        
        