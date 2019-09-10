from django.contrib import admin

from user.models import User
from user.forms import UserForm


class UserAdmin(admin.ModelAdmin):
    form = UserForm

    list_display = ['first_name', 'last_name', 'iban']
    search_fields = ['first_name', 'last_name', 'iban']

admin.site.register(User, UserAdmin)