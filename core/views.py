import email
from pyexpat import model
from django.shortcuts import render
from rest_framework import views as rest_views
from rest_framework import response as rest_response
from rest_framework import status as rest_status

from core import serializers as core_serializers
from core import models as core_models
# Create your views here.


class RegisterAPiView(rest_views.APIView):

    def post(self, request):


        serializer_instance = core_serializers.RegisterSerializers(data=request.data)

        if not serializer_instance.is_valid():
            return rest_response.Response(data=serializer_instance.errors, status=rest_status.HTTP_400_BAD_REQUEST)

        email = serializer_instance.validated_data.get('email')

        user = core_models.User.objects.create(
            username=serializer_instance.validated_data.get("username"),
            mobile = serializer_instance.validated_data.get("mobile"),
            password = serializer_instance.validated_data.get("mobile"),
        )

        if user:
            core_models.UserEmail.objects.create(email=email, user=user)
        # core_serializers
        return rest_response.Response(data={"data":user.get_details()}, status=rest_status.HTTP_200_OK)