from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    email = models.EmailField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  

    def set_password(self, raw_password):
        """Hashes and stores the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verifies a password against the stored hash."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email

from django.db import models
from decimal import Decimal

class SkillAd(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rate = models.DecimalField(max_digits=6, decimal_places=2)
    available_days = models.CharField(max_length=100)

    @property
    def platform_fee(self):
        return self.rate * Decimal('0.15')

    @property
    def user_earnings(self):
        return self.rate * Decimal('0.85')  # 15% taken by platform

    def __str__(self):
        return f"{self.title} by {self.user.name}"

