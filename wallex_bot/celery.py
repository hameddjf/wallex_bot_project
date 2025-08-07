import os
from celery import Celery
from celery.schedules import crontab

# تنظیم متغیر محیطی پیش‌فرض برای ماژول تنظیمات جنگو
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wallex_bot.settings')

# ایجاد یک نمونه از اپلیکیشن Celery
app = Celery('wallex_bot')

# خواندن تنظیمات از فایل settings.py جنگو
# تمام متغیرهای با پیشوند CELERY_ در settings.py خوانده می‌شوند
app.config_from_object('django.conf:settings', namespace='CELERY')

# بارگذاری خودکار ماژول‌های tasks.py از تمام اپلیکیشن‌های ثبت شده در جنگو
app.autodiscover_tasks()