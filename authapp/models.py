from datetime import date

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='static/img/avatars/', blank=True)

    def has_active_subscription(self):
        subscription = self.subscriptions.filter(expiry_date__gte=date.today()).first()
        return subscription.subscription_type

    def __str__(self):
        return self.username
