from django.db import models
from django.db.models.signals import post_save


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
        super().save(*args, **kwargs)


def address_save(sender, instance, **kwargs):
    other_address = UserAddress.objects.filter(user=instance.user).exclude(pk=instance.pk)
    to_remove = set()
    equal = True
    if other_address:
        for address in other_address:
            if address.street_address_line2 and instance.street_address_line2:
                if address.street_address_line2.lower() == instance.street_address_line2.lower():
                    pass
                else:
                    equal = False
                    if instance.street_address_line2 in address.street_address_line2:
                        to_remove.add(instance.pk)
                        break
                    elif address.street_address_line2 in instance.street_address_line2:
                        to_remove.add(address.pk)
                        continue
                    else:
                        continue
            elif address.street_address_line2:
                to_remove.add(instance.pk)
                break
            elif instance.street_address_line2:
                to_remove.add(address.pk)
                continue

            if address.street_address and instance.street_address:
                if address.street_address.lower() == instance.street_address.lower():
                    pass
                else:
                    equal = False
                    if instance.street_address in address.street_address:
                        to_remove.add(instance.pk)
                        break
                    elif address.street_address in instance.street_address:
                        to_remove.add(address.pk)
                        continue
                    else:
                        continue
            elif address.street_address:
                to_remove.add(instance.pk)
                break
            elif instance.street_address:
                to_remove.add(address.pk)
                continue

            if address.zipcode and instance.zipcode:
                if address.zipcode.lower() == instance.zipcode.lower():
                    pass
                else:
                    equal = False
            elif address.zipcode:
                to_remove.add(instance.pk)
                break
            elif instance.zipcode:
                to_remove.add(address.pk)
                continue

            if address.city and instance.city:
                if address.city.lower() == instance.city.lower():
                    pass
                else:
                    equal = False
            elif address.city:
                to_remove.add(instance.pk)
                break
            elif instance.city:
                to_remove.add(address.pk)
                continue

            if address.state and instance.state:
                if address.state.lower() == instance.state.lower():
                    pass
                else:
                    equal = False
            elif address.state:
                to_remove.add(instance.pk)
                break
            elif instance.state:
                to_remove.add(address.pk)
                continue

            if address.country and instance.country:
                if address.country.lower() == instance.country.lower():
                    pass
                else:
                    equal = False
            elif address.country:
                to_remove.add(instance.pk)
                break
            elif instance.country:
                to_remove.add(address.pk)
                continue

            if equal:
                to_remove.add(instance.pk)

    UserAddress.objects.filter(pk__in=to_remove).delete()


post_save.connect(address_save, sender=UserAddress)
