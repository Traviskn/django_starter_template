import uuid
import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# See: https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#specifying-a-custom-user-model


class UserManager(BaseUserManager):
    """
    Custom model manager for the account object.
    """

    def create_user(self, email, username, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')
        if not username:
            raise ValueError('Users must have a valid username.')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.username = username
        user.is_active = True
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, username, password, **kwargs):
        user = self.create_user(email, username, password)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user object, extended from the built-in django user.
    """

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(
        'username',
        max_length=30,
        unique=True,
        db_index=True,
        help_text='30 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.',
                'invalid'
            ),
        ],
        error_messages={
            'unique': "A user with that username already exists.",
        }
    )

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # A list of the field names that will be prompted for when
    # creating a user via the createsuperuser management command.
    # should not contain the USERNAME_FIELD or password as these
    # fields will always be prompted for.
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return '{name} <{email}>'.format(
            name=self.get_full_name(),
            email=self.email,
        )

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def verify_user_email(self, request):
        # ensure this user object has been saved to the database to prevent exception while creating SecurityDetails
        self.save()
        try:
            security_details = SecurityDetails.objects.get(user=self)
        except SecurityDetails.DoesNotExist:
            security_details = SecurityDetails()
            security_details.user = self
        security_details.send_verification_link(request)


class SecurityDetails(models.Model):
    """
    Stores a security token with an expiration date to verify a new user's email.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    token = models.CharField(max_length=40)
    token_expiration = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'token')

    def send_verification_link(self, request):
        self.token = uuid.uuid4()
        self.token_expiration = timezone.now() + datetime.timedelta(days=3)
        protocol = 'https' if request.is_secure() else 'http'
        domain = get_current_site(request).domain
        verification_link = protocol + '://' + domain + reverse('accounts:verify', args=(self.user.email, self.token,))
        subject = 'Account Activation'
        message = 'Thank you for signing up at ' + domain + '! Follow this link to verify your email: \n' + verification_link
        self.user.email_user(subject, message, settings.EMAIL_HOST_USER, fail_silently=False)
        self.save()

    def is_token_valid(self, mail_token):
        if self.token == mail_token:
            if timezone.now() < self.token_expiration:
                self.user.is_active = True
                self.user.save()
                return True
        return False
