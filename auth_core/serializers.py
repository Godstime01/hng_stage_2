from rest_framework import serializers
from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("userId", "first_name", "last_name", "email", "phone", "password")
        extra_kwargs = {"password": {"write_only": True}, "userId": {"read_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        return user
