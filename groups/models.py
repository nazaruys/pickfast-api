from django.db import models
from django.utils.crypto import get_random_string
from django.conf import settings
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from core.signals import reset_group_admin_signal

User= get_user_model()


class Group(models.Model):
    code = models. \
        CharField(
            max_length=6,
            unique=True, 
            blank=True, 
            editable=False, 
            primary_key=True)
    
    admin = models. \
        OneToOneField(
            User, 
            null=True, 
            related_name='admin_of', 
            on_delete=models.SET_NULL)
    
    @receiver(pre_delete, sender=User)
    def resign_admin(sender, instance, **kwargs):
        group_of_admin = instance.admin_of
        # If user is an admin
        if group_of_admin is not None:
            group_of_admin.admin = group_of_admin.members.exclude(pk=instance.pk).first()
            group_of_admin.save()

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        allowed_chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        code = get_random_string(length=6, allowed_chars=allowed_chars)
        while Group.objects.filter(code=code).exists():
            code = get_random_string(length=6, allowed_chars=allowed_chars)
        return code
    
    def reset_group_admin(sender, instance, **kwargs):
        group = instance.admin_of
        group.admin = group.members.exclude(pk=instance.pk).first()
        group.save()
        if group.admin == None:
            group.delete()

    reset_group_admin_signal.connect(reset_group_admin)

class Store(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, null=True, related_name='stores', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    PRIORITY_CHOICES = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High')
    ]

    title = models.CharField(max_length=40)
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    active = models.BooleanField(default=True)
    store = models.ForeignKey(Store, null=True, on_delete=models.CASCADE, related_name='products')
    group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name='products')
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.title
    
