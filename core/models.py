from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def delete(self, *args, **kwargs):
        raise ValidationError("This model instance cannot be deleted.")