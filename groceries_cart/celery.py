import os
from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'groceries_cart.settings')

celery = Celery('groceries_cart')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

celery.conf.beat_schedule = {
    'cleanup-old-products': {
        'task': 'groups.tasks.cleanup_old_products',
        'schedule': crontab(hour=0, minute=0),
    },
}