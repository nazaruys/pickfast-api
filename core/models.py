from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    name = models.CharField(max_length=30, null=True)
    email = models.EmailField(unique=True)
    group = models.ForeignKey('groups.Group', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    first_name = None
    last_name = None
    last_login = None

    def delete(self, *args, **kwargs):
        raise ValidationError("This model instance cannot be deleted.")
    
    def get_short_name(self):
        return self.name
    
    def get_full_name(self):
        return self.name