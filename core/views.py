import email
from pyexpat import model
from turtle import update
from django.shortcuts import render
from django.utils import timezone
from rest_framework import views as rest_views
from rest_framework import response as rest_response
from rest_framework import status as rest_status
from django.core.cache import cache

from core import serializers as core_serializers
from core import models as core_models
from django.conf import settings as dj_settings
from core import utils as core_utils
from rest_framework.authtoken import models as token_models
from rest_framework.permissions import IsAuthenticated

import core

# Create your views here.


class RegisterAPiView(rest_views.APIView):

    def post(self, request):


        serializer_instance = core_serializers.RegisterSerializers(data=request.data)

        if not serializer_instance.is_valid():
            return rest_response.Response(data=serializer_instance.errors, status=rest_status.HTTP_400_BAD_REQUEST)

        emails = serializer_instance.validated_data.get('emails')
        mobile = serializer_instance.validated_data.get("mobile")
        user, created = core_models.User.objects.get_or_create(
            mobile = mobile
        )

        if not created and not user.mobile:
            created = True
        else:
            user.password = serializer_instance.validated_data.get("password")
            user.username = serializer_instance.validated_data.get("username")

            user.save(update_fields = ["password", "username"])
            for obj in emails:
                if not core_models.UserEmail.objects.filter(email=obj.get("email"), user=user).exists():
                    core_models.UserEmail.objects.create(
                        email=obj.get("email"), 
                        user=user, 
                        is_primary=obj.get("is_primary")
                        )

        sms_otp = ""
        if mobile not in dj_settings.OTP_IGNORE_MOBILE:
            if not user.is_user_blocked:
                if not cache.get(mobile):
                    sms_otp = core_utils.send_otp(
                            mobile
                        )
                    cache.set("otp_%s" % mobile, sms_otp, timeout=300)
                    user.number_of_attempt = 0
                    user.save(update_fields=['number_of_attempt'])
            else:
                if user.is_user_blocked and user.otp_block_time < timezone.now():
                    user.number_of_attempt = 0
                    user.is_user_blocked = False
                    user.save(update_fields=['number_of_attempt', "is_user_blocked"])
                return rest_response.Response(data={"data":"Your maximum 3 attempt exceed please wait for five minutes"}, status=rest_status.HTTP_400_BAD_REQUEST)

        core_utils.user_send_mail(user)
        return rest_response.Response(data={"data":user.get_details()}, status=rest_status.HTTP_200_OK)


class LoginAPIView(rest_views.APIView):
    
    def post(self, request):
        serializer_instance = core_serializers.OTPVerifySerializer(data=request.data)
        if not serializer_instance.is_valid():
            return rest_response.Response(
                data = {"data":serializer_instance.errors}, 
                status = rest_status.HTTP_400_BAD_REQUEST
            )

        user_instance = serializer_instance.validated_data.get("user_id")
        user_otp_serializer_instance = core_serializers.UserOTPVerifySerializer(
            data=request.data, context={"mobile": user_instance.mobile}
        )
        if not user_otp_serializer_instance.is_valid():
            return rest_response.Response(
                data = {"data":user_otp_serializer_instance.errors}, 
                status = rest_status.HTTP_400_BAD_REQUEST
            )

        user_instance.is_mobile_verified = True
        user_instance.is_user_blocked = False
        user_instance.save(update_fields=["is_mobile_verified", "is_user_blocked"])

        token_instance = token_models.Token.objects.filter(user=user_instance).last()
        if token_instance:
            token_instance.delete()

        token_instance, _ = token_models.Token.objects.get_or_create(user=user_instance)
        return rest_response.Response(
            data = {"token": token_instance.key},
            status=rest_status.HTTP_200_OK,
        )

class UserProfileAPiView(rest_views.APIView):
    permission_classes = [IsAuthenticated,]

    def post(self, request):
        pass


        
        