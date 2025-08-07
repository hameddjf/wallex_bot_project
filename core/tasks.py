from celery import shared_task
from .services import get_specific_crypto_data
import logging
import pprint
import json

logger = logging.getLogger(__name__)

@shared_task
def fetch_and_log_specific_crypto_data():
    """
    این وظیفه توسط Celery Beat به صورت دوره‌ای اجرا می‌شود.
    داده‌های ارزهای مشخص شده بر پایه تومان را دریافت کرده
    و نتیجه را در یک فایل JSON ذخیره می‌کند.
    """
    logger.info("="*50)
    logger.info("شروع وظیفه زمان‌بندی شده: دریافت اطلاعات و ذخیره در فایل JSON...")
    
    data = get_specific_crypto_data()
    
    print("\n--- نتیجه دریافت شده از سرویس ---")
    pprint.pprint(data)
    print("---------------------------------\n")

    file_path = "specific_crypto_data.json"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        logger.info(f"اطلاعات با موفقیت در فایل '{file_path}' ذخیره شد.")
    
    except Exception as e:
        logger.error(f"خطا در هنگام ذخیره اطلاعات در فایل JSON: {e}")
        return f"وظیفه با خطا در ذخیره‌سازی فایل خاتمه یافت: {e}"

    logger.info("پایان وظیفه.")
    
    if 'error' in data or 'message' in data:
        return f"وظیفه با پیام خاتمه یافت: {data}"
    else:
        return f"اطلاعات برای {len(data)} بازار با موفقیت دریافت و در فایل JSON ذخیره شد."





    










# run cmd as admistrator

# celery -A wallex_bot worker -l info -P solo
# celery -A wallex_bot beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler

# cd C:\Users\H_M\Desktop\ON GOING PROJECTS\wallex_bot_project

# اجرا کردن سرور ردیس
# cd C:\Users\H_M\Downloads\Programs\Redis-x64-3.0.504
# redis-server.exe
# در ترمینال دیگر برای اطمینان از اتصال به ردیس
# redis-cli.exe ping

# cmd redis-server --service-install redis.windows-service.conf
# cmd redis-server --service-start
# redis-cli
# ping

# run 
# 