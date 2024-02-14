
from base64 import urlsafe_b64decode, urlsafe_b64encode
from django.urls import reverse
from rest_framework import serializers, generics
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = User
        fields = ['username','password','image','first_name','last_name','about_me','gender','marital_status','wedding_date','birth_date','blood_group','personal_email','email',
                  'pan_number','aadhar_number','aadhar_name','aadhar_image','pan_image','created_at','modified_at','deleted_at','is_admin_user','is_active','is_verified']


    def create(self, validated_data):
        return User.objects.create_user(validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class LoginSerializer(serializers.Serializer):
    """
    Serializer  for user login
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['username', 'password']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')