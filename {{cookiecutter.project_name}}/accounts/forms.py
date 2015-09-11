from django import forms
# See: https://docs.djangoproject.com/en/1.8/topics/auth/default/#built-in-forms
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm as BaseUserChangeForm
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm as BasePasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from .models import User


class UserCreationForm(BaseUserCreationForm):
    """
    Custom form for creating new users.
    """
    username = forms.RegexField(
        label="Username",
        max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text="",
        error_messages={
            'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."
        },
        widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email',)
        widgets = {
            'email': forms.widgets.EmailInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match.')
        return password2

    def save(self, commit=True):
        # Save the provided user password in hashed format
        user = super(BaseUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(BaseUserChangeForm):
    """
    Custom form for updating an existing user.
    """
    password = ReadOnlyPasswordHashField(label='Password',
                                         help_text="""Raw passwords are not stored, so there is no way to see this
                                         user's password, but you can change the password using
                                         <a href=\"/accounts/password_change/\">this form</a>.""")

    class Meta(BaseUserChangeForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'user_permissions'
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial['password']

    # TODO: Raise a validation error if the attempted username or email is
    #       already taken. We need to exclude the current user from the check.
    #       Currently a 500 error should occur.


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )
        widgets = {
            'first_name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.widgets.TextInput(attrs={'class': 'form-control'}),
        }


class AuthenticationForm(BaseAuthenticationForm):
    """
    Custom Login Form.
    """

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class PasswordChangeForm(BasePasswordChangeForm):
    """
    Custom form for allowing a user to change their password.
    """

    old_password = forms.CharField(
        label='Old password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class PasswordResetForm(BasePasswordResetForm):
    """
    Custom form for generating and emailing a one-time use link to reset a user’s password
    """

    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def get_users(self, email):
        """
        Given an email, return matching user(s) who should receive a reset.
        Allow users with unusable passwords (social auth users) to reset their password.
        This will allow social auth users to use the forgot password link to create a password
        and login like normal users.
        """
        active_users = get_user_model()._default_manager.filter(email__iexact=email, is_active=True)
        print(active_users)
        return (u for u in active_users)


class SetPasswordForm(BaseSetPasswordForm):
    """
    Custom form that lets a user change their password without entering the old password.
    """

    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
