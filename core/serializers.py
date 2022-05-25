from email.policy import default
from xml.dom import ValidationErr
from rest_framework import serializers
from core import models as core_models
from django.conf import settings as dj_settings
from django.core.cache import cache
from django.utils import timezone
from datetime import datetime, timedelta

import core


class UserEmails(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    is_primary = serializers.BooleanField(default=False)
class RegisterSerializers(serializers.Serializer):
    emails = UserEmails(many=True)
    mobile = serializers.CharField(max_length=14)
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)

class OTPVerifySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    otp = serializers.IntegerField(min_value=1, max_value=9999)

    def validate_user_id(self, value):
        user = core_models.User.objects.filter(id=value).last()
        if not user:
            raise serializers.ValidationError("Invalid user id")

        return user


class UserOTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=40)

    def validate_otp(self, value):
        mobile = self.context.get("mobile")
        if mobile in dj_settings.OTP_IGNORE_MOBILE and str(value) == "1234":
            return value
        cache_otp = cache.get("otp_%s" % mobile)
        print("cache_otp=====>", cache_otp)
        print("str(value)=====>", str(value))
        if str(cache_otp) != str(value):
            user_instace = core_models.User.objects.filter(mobile=mobile).last()
            if user_instace.number_of_attempt >= 3:
                user_instace.otp_block_time = timezone.now() + timedelta(minutes=5)
                user_instace.save(update_fields=['otp_block_time'])
                raise serializers.ValidationError("Your maximum 3 attempt exceed please wait for five minutes")
            else:
                user_instace.number_of_attempt +=1
                user_instace.save(update_fields=['number_of_attempt'])
                
                if user_instace.number_of_attempt >= 3:
                    user_instace.is_user_blocked=True
                    user_instace.otp_block_time = timezone.now() + timedelta(minutes=5)
                    user_instace.save(update_fields=['is_user_blocked', 'otp_block_time'])
            raise serializers.ValidationError("Invalid OTP")

        return value
