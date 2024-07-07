from rest_framework import serializers
from .models import UserModel


def custom_error_response(errors):
    print(errors)

    error_list = []
    for field, messages in errors.items():
        for message in messages:
            error_list.append({"field": field, "message": message})
    return {"errors": error_list}


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
