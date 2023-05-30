from rest_framework import serializers 
from django.conf import settings
from g_auth.models import G_AUTH_USER_MODEL
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt import serializers as jwt_serializers
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken


class GUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = G_AUTH_USER_MODEL(
            email = validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            role=validated_data['role']
            
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 
    
    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.date_of_birth = validated_data['date_of_birth']
        instance.role = validated_data['role']
        instance.save()

class TokenObtainPairSerializer(jwt_serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Custom claims
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["role"] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh["exp"]
        data['access'] = str(refresh.access_token)
        data['access_expires'] = refresh.access_token["exp"]

        return data


class TokenRefreshSerializer(serializers.Serializer):
    # Instead of inputting the refresh token from the HTTP body, we pull it
    # from the cookie

    def get_token_from_cookie(self):
        request = self.context["request"]
        return request.COOKIES.get(settings.JWT_COOKIE_NAME)

    def validate(self, attrs):
        token = self.get_token_from_cookie()
        if token is None:
            raise serializers.ValidationError(
                "No refresh token cookie found"
            )
        refresh = RefreshToken(token)

        data = {
            "access": str(refresh.access_token),
            "access_expires": refresh.access_token["exp"]
        }

        if jwt_settings.BLACKLIST_AFTER_ROTATION:
            try:
                # Attempt to blacklist the given refresh token
                refresh.blacklist()
            except AttributeError:
                # If blacklist app not installed, `blacklist` method will
                # not be present
                pass

        refresh.set_jti()
        refresh.set_exp()

        data['refresh'] = str(refresh)
        data['refresh_expires'] = refresh["exp"]

        return data