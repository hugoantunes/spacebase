from django.contrib import admin

from user.models import User, UserAddress
from user.forms import UserForm


class UserAddressInline(admin.StackedInline):
    model = UserAddress
    fk_name = "user"
    extra = 0


class UserAdmin(admin.ModelAdmin):
    form = UserForm

    search_fields = ['first_name', 'last_name']
    inlines = [
        UserAddressInline,
    ]

    def hide_iban(self, obj):
        return f"---{obj.iban[-4:]}"
    hide_iban.short_description = 'iban'

    def get_list_display(self, request):
        display_list = ('first_name', 'last_name')
        if request.user.is_superuser:
            return display_list + ('iban',)
        else:
            return display_list + ('hide_iban',)


admin.site.register(User, UserAdmin)
