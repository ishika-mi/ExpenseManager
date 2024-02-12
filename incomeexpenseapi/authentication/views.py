import os
from django.http import HttpResponsePermanentRedirect
from rest_framework import views, permissions
from .services import LoginService, RegisterService, VerifyEmailService, LogoutService
from .serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, LogoutSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class RegisterView(views.APIView):
    serializer_class = RegisterSerializer
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        RegisterService(request,self.serializer_class).post_register_service()


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        return VerifyEmailService(request,self.serializer_class).get_verify_email()


class LoginAPIView(views.APIView):
    serializer_class = LoginSerializer
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        return LoginService(request,self.serializer_class).post_login_view()


class LogoutAPIView(views.APIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        return LogoutService(request,self.serializer_class)
