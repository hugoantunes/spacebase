from django.test import TestCase
from user.models import UserAddress, User


class UserAddressTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='hugo',
            last_name='antunes',
            iban='12345678',
        )

    def test_new_addresses_should_be_kept(self):
        UserAddress(user=self.user, name="Max", city="Giventown").save()

        self.assertEqual(1, UserAddress.objects.all().count())

    def test_after_save_address_should_keep_different_address(self):
        UserAddress(user=self.user, name="Max", city="Giventown").save()
        add2 = UserAddress(user=self.user, name="Max Mustermann", street_address="Randomstreet", city="Giventown")
        add2.save()
        add3 = UserAddress(user=self.user, name="Max Mustermann", street_address="456 Randomstreet", city="Giventown")
        add3.save()
        add4 = UserAddress(
            user=self.user, name="Max Mustermann", street_address="789 Otherstreet", city="Giventown", country="NL"
        )
        add4.save()
        addresses = UserAddress.objects.all()

        self.assertEqual(2, addresses.count())
        self.assertNotIn(add2, addresses)
        self.assertIn(add3, addresses)
        self.assertIn(add4, addresses)

    def test_after_save_address_should_keep_most_specific_address(self):
        UserAddress(user=self.user, name="Max", city="Giventown").save()
        add2 = UserAddress(user=self.user, name="Max Mustermann", street_address="Randomstreet", city="Giventown")
        add2.save()
        add3 = UserAddress(user=self.user, name="Max Mustermann", street_address="456 Randomstreet", city="Giventown")
        add3.save()
        add4 = UserAddress(
            user=self.user, name="Max Mustermann", street_address="456 Randomstreet", city="Giventown", country="NL"
        )
        add4.save()
        addresses = UserAddress.objects.all()

        self.assertEqual(1, addresses.count())
        self.assertNotIn(add2, addresses)
        self.assertNotIn(add3, addresses)
        self.assertIn(add4, addresses)
