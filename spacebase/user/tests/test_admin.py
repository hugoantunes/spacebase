from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from user.models import User as ClientUser
from user.admin import UserAdmin


class MockRequest:
    pass


class MockSuperUser:

    @property
    def is_superuser(self):
        return True


class MockUser:

    @property
    def is_superuser(self):
        return False


request = MockRequest()
request.user = MockSuperUser()


class ModelAdminTests(TestCase):

    def setUp(self):
        self.user = ClientUser.objects.create(
            first_name='hugo',
            last_name='antunes',
            iban='12345678',
        )
        self.site = AdminSite()

    def test_hide_iban_should_mask_full_user_iban(self):
        admin = UserAdmin(ClientUser, self.site)
        self.assertEqual(admin.hide_iban(self.user), '---5678')

    def test_super_users_should_see_iban_field_instead_hide_iban(self):
        admin = UserAdmin(ClientUser, self.site)
        self.assertEqual(list(admin.get_list_display(request)), ['first_name', 'last_name', 'iban'])

        request.user = MockUser()
        self.assertEqual(list(admin.get_list_display(request)), ['first_name', 'last_name', 'hide_iban'])
