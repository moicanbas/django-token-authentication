from rest_framework import serializers
from djoser.serializers import UserSerializer, UserCreateSerializer as BaseUserSerializer


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

class BaseSerializer(serializers.ModelSerializer):
    model = None
    fields = None

    class Meta:
        model = None
        fields = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.model = self.model
        self.Meta.fields = self.fields