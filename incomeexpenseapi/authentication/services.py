from datetime import datetime
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.hashers import check_password
import jwt
from django.db.models import Q
from authentication.mailchimp_utils import mark_user_as_subscribed_in_mailchimp, send_email_using_mailchimp
from rest_framework.response import Response
from rest_framework import generics, status, views, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError

from incomeexpenseapi.settings import SIMPLE_JWT
from .models import User
from .utils import Util, get_tokens_for_user


class RegisterService:
    def __init__(self, request,serializer_class):
        self.request = request
        self.serializer_class = serializer_class

    def post_register_service(self):
        user = self.request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(self.request).domain
        relativeLink = reverse('email-verify')
        absurl = f'http://{current_site}{relativeLink}?token={str(token)}'
        email_body = f'Hi {user.username} Use the link below to verify your email \n{absurl}'
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}
        ######################################################## SEND MAIL USING MAILCHIMP ####################################################################
        #### Use below given method to send mail using mailchimp. 
        #### NOTE: First verify Domain in mailchimp before sending email check below given link
        ##### https://mailchimp.com/developer/transactional/guides/send-first-email/
        # send_email_using_mailchimp(to_email = user.email,username = user.username, url = absurl)
        ######################################################################################################################################################
        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)
    
class VerifyEmailService:
    def __init__(self, request,serializer_class):
        self.request = request
        self.serializer_class = serializer_class
    
    def get_verify_email(self):
        token = self.request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY,algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                ########################################################### MARK USER AS SUBSCRIBED IN MAILCHIMP ######################################################
                # mark_user_as_subscribed_in_mailchimp(user.email)
                #######################################################################################################################################################
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except (jwt.exceptions.DecodeError, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginService:
    def __init__(self, request,serializer_class):
        self.request = request
        self.serializer_class = serializer_class
    
    def post_login_view(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        username = self.request.data.get('username')
        password = self.request.data.get('password')
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist as e:
            raise ValidationError('NO_USER_FOUND') from e
        if not check_password(password, user.password):
            raise ValidationError('INVALID_CREDENTIALS')
        if (not user.is_active or not user.is_verified) and (user.is_active or user.is_verified):
            raise ValidationError('NO_USER_FOUND')
        data = get_tokens_for_user(user)

        now = datetime.utcnow()

        # Calculate the expiry time based on the ACCESS_TOKEN_LIFETIME in the SIMPLE_JWT settings
        expiry_time = now + SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        return Response(data,  status=status.HTTP_200_OK)

        # return Response(serializer.data, status=status.HTTP_200_OK)
    

class LogoutService:
    def __init__(self, request,serializer_class):
        self.request = request
        self.serializer_class = serializer_class
    
    def post_logout_view(self):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)