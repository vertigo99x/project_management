from .models import User
from rest_framework import serializers 



class UserSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email','role', 'first_name', 'last_name', 'profile_image_url', 'is_active','date_joined',]

    def get_profile_image_url(self, obj):
        return obj.get_profile_image()
    
