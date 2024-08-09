from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'identification',
                  'first_name', 'last_name', 'email', 'groups', 'user_permissions']
