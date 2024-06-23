from celery import shared_task
from django.utils import timezone
from .models import Product

@shared_task
def cleanup_old_products():
    print("Starting cleaning up old products.")
    threshold_date = timezone.now() - timezone.timedelta(days=28)
    old_products = Product.objects.filter(date_buyed__lt=threshold_date)
    old_products.delete()
    print("Deleted old products.")