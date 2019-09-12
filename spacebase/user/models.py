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

    @classmethod
    def dedupublicate_address(cls, old, new, attr, subset=False):
        new_address_attr = getattr(new, attr)
        old_address_attr = getattr(old, attr)
        if old_address_attr and new_address_attr:
            if old_address_attr.lower() != new_address_attr.lower():
                equal = False
                if subset:
                    return cls.find_subset(
                        new_address_attr, old_address_attr, new, old
                    )
        elif old_address_attr:
            return new.pk, 0, False
        elif new_address_attr:
            return old.pk, 1, False
        return None, None, True

    @classmethod
    def find_subset(clas, new_address_attr, old_address_attr, new, old):
        if new_address_attr.lower() in old_address_attr.lower():
            return new.pk, 0, False
        elif old_address_attr.lower() in new_address_attr.lower():
            return old.pk, 1, False
        else:
            return None, 1, False

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
            for attr in ['street_address_line2', 'street_address']:
                pk, statment, equal = UserAddress.dedupublicate_address(
                    instance, address, attr, subset=True
                )
                if pk:
                    to_remove.add(pk)
            if not equal:
                if statment:
                    continue
                else:
                    break
            for attr in ['zipcode', 'city', 'state', 'country']:
                pk, _, equal = UserAddress.dedupublicate_address(instance, address, attr)
                if pk:
                    to_remove.add(pk)

            if equal:
                to_remove.add(instance.pk)

    UserAddress.objects.filter(pk__in=to_remove).delete()


post_save.connect(address_save, sender=UserAddress)
