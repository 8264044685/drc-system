from xml.dom import ValidationErr
from rest_framework import serializers
from core import models as core_models

class RegisterSerializers(serializers.Serializer):
    # emails = serializers.ListField(child = serializers.EmailField(max_length=100))
    email = serializers.EmailField(max_length=100)
    mobile = serializers.CharField(max_length=14)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)

    def validate(self, validated_data):

        if core_models.User.objects.filter(mobile=validated_data.get('mobile')).exists():
            raise serializers.ValidationError("mobile number is already register")
        return validated_data
        