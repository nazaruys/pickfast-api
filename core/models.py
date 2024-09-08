import random
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    verified = models.BooleanField(default=False, blank=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    first_name = None
    last_name = None
    last_login = None

    def save(self, *args, **kwargs):
        if self.pk:
            original_email = User.objects.get(pk=self.pk).email
            if self.email != original_email:
                # Email is being changed, so reset verification status and generate a new code
                self.verified = False
                self.verification_code = f'{random.randint(100000, 999999)}'

        # Generate verification code for new users or when no code exists
        if not self.verification_code and not self.verified:
            self.verification_code = f'{random.randint(100000, 999999)}'

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("This model instance cannot be deleted.")
    
    def get_short_name(self):
        return self.name
    
    def get_full_name(self):
        return self.name