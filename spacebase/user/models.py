from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    iban = models.CharField(max_length=34, blank=False)


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    street_address_line2 = models.CharField(max_length=255, blank=True, null=True)
    zipcode = models.CharField(max_length=12, blank=True, null=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=2)
    full_address = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        streetdata = f"{self.street_address}\n{self.street_address_line2}"
        self.full_address = f"{streetdata}\n{self.zipcode} {self.city} {self.state} {self.country}"
        super(UserAddress).save(*args, **kwargs)
