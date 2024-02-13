from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, MinLengthValidator, \
    FileExtensionValidator
from datetime import date
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):

    def create_user(self, validated_data):
        user = self.model(
            username=validated_data.get('username'),
            email=self.normalize_email(validated_data.get('email')),
            first_name=validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            about_me = validated_data.get('about_me'),
            gender = validated_data.get('gender'),
            marital_status = validated_data.get('marital_status'),
            birth_date = validated_data.get('birth_date'),
            blood_group = validated_data.get('blood_group'),
            personal_email = validated_data.get('personal_email'),
            pan_number = validated_data.get('pan_number'),
            aadhar_number = validated_data.get('aadhar_number'),
            aadhar_name = validated_data.get('aadhar_name'),
            is_admin_user = validated_data.get('is_admin_user', False),
            is_active = validated_data.get('is_active', False),
            is_verified = validated_data.get('is_verified', False),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    genders = (
        ('female', 'Female'),
        ('male', 'Male'),
        ('other', 'Other'),
    )
    blood_groups = (
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('NULL', None),
    )
    marital_statuses = (
        ('married', 'Married'),
        ('unmarried', 'Unmarried'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('NULL', None),
    )
    employee_types = (
        ('internal', 'Internal'),
        ('external', 'External')
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        help_text=(
            "Required. characters length between (2,50). Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator, MinLengthValidator(2)],
        error_messages={
            "unique": 'A user with that username already exists.',
        },
    )

    image = models.ImageField(upload_to='profiles', blank=True, null=True,
                              validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message='First name should contains characters only !',
        code='first_name'
    )])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2), RegexValidator(
        regex='^[a-zA-Z]+$',
        message='Last name should contains characters only !',
        code='last_name'
    )])
    about_me = models.TextField(null=True, blank=True)

    gender = models.CharField(max_length=10, choices=genders)
    marital_status = models.CharField(max_length=20, choices=marital_statuses, default=None, null=True)
    wedding_date = models.DateField(blank=True, null=True, validators=[MaxValueValidator(limit_value=date.today)])
    birth_date = models.DateField(blank=True, null=True, validators=[MaxValueValidator(limit_value=date.today)])
    blood_group = models.CharField(max_length=5, choices=blood_groups, default=None, null=True)

    personal_email = models.EmailField(unique=True, null=True)
    email = models.EmailField(unique=True)

    pan_number = models.CharField(max_length=10, null=True, unique=True, validators=[RegexValidator(
        regex='[A-Za-z]{5}\d{4}[A-Za-z]{1}',
        message='Pan number is invalid !',
        code='pan_number'
    )])
    aadhar_number = models.CharField(max_length=12, null=True, unique=True, validators=[RegexValidator(
        regex='^[2-9]{1}[0-9]{3}[0-9]{4}[0-9]{4}$',
        message='Aadhar number is invalid !',
        code='aadhar_number'
    )])
    aadhar_name = models.CharField(max_length=50, blank=True, null=True, validators=[RegexValidator(
        regex='^[a-zA-Z\s]+$',
        message='Aadhar name should contains characters only !',
        code='aadhar_name'
    )])
    aadhar_image = models.ImageField(upload_to='aadhar', blank=True, null=True,
                                     validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])
    pan_image = models.ImageField(upload_to='pan', blank=True, null=True,
                                  validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])])


    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    is_admin_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = 'AuthUsers'

    def __str__(self):
        return f"{self.username}-{self.id}"
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }