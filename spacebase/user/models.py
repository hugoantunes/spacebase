from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    iban = models.CharField(max_length=34, blank=False)
