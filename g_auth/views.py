from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from django.contrib.auth import get_user_model
from g_auth.serializers import GUserSerializer
from g_auth.models import G_AUTH_USER_MODEL

from django.utils.timezone import datetime
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import (
    RefreshToken as RefreshTokenModel
)
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from . import serializers
# from g_auth.utils import get_custom_jwt


# Two-Factor Authentication 
def get_user_totp_device(self, user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device   

class TOTPCreateView(APIView):
    """
    Use this endpoint to set up a new TOTP Device
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)

class TOTPVerifyView(APIView):
    """
    This endpoint allows users to verify/enable a TOTPDevice
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(self, user)
        if not device:
            return Response(dict(errors=['This user has not enabled/ setup two factor authentication']), status=status.HTTP_400_BAD_REQUEST)
        
        if not device == None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
                user.is_two_factor_enabled = True
                user.save()
            # token = get_custom_jwt(user, device)
            return Response({'toke': token}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Create your views here.

class UserViewset(ModelViewSet):
    queryset = settings.AUTH_USER_MODEL
    serializer_class = GUserSerializer()

    def perform_create(self, serializer):
        serializer.save()

class TokenViewBaseWithCookie(TokenViewBase):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        resp = Response(serializer.validated_data, status=status.HTTP_200_OK)

        # TODO: this should probably be pulled from the token exp
        expiration = (datetime.utcnow()+jwt_settings.REFRESH_TOKEN_LIFETIME)

        resp.set_cookie(
            settings.JWT_COOKIE_NAME,
            serializer.validated_data["refresh"],
            expires=expiration,
            secure=settings.JWT_COOKIE_SECURE,
            httponly=True,
            samesite=settings.JWT_COOKIE_SAMESITE
        )

        return resp


class Login(TokenViewBaseWithCookie):
    serializer_class = serializers.TokenObtainPairSerializer


class RefreshToken(TokenViewBaseWithCookie):
    serializer_class = serializers.TokenRefreshSerializer


class Logout(APIView):

    def post(self, *args, **kwargs):
        resp = Response({})
        token = self.request.COOKIES.get(settings.JWT_COOKIE_NAME)
        refresh = RefreshTokenModel(token)
        refresh.blacklist()
        resp.delete_cookie(settings.JWT_COOKIE_NAME)
        return resp