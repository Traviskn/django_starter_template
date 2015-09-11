from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    """
    The user's representation in the admin interface.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined',)
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    fieldsets = (
        ('Account', {'fields': ('username', 'email', 'password', 'first_name', 'last_name', 'date_joined',)}),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active',)
        }),
    )

    search_fields = ('email',)
    ordering = ('date_joined', 'email', 'username',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
