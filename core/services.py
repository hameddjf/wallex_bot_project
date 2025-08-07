# Logic related to interaction with wallex
import requests
from django.conf import settings

# آدرس پایه API والکس
BASE_URL = "https://api.wallex.ir/v1"

def get_all_markets_data():
    """
    این تابع اطلاعات تمام بازارهای موجود در والکس را دریافت می‌کند.
    """
    # آدرس کامل برای دریافت اطلاعات بازارها
    url = f"{BASE_URL}/markets"
    
    # کلید API از تنظیمات جنگو خوانده می‌شود
    api_key = settings.WALLEX_API_KEY
    
    # هدرهای مورد نیاز برای احراز هویت
    # نکته: فرمت دقیق هدر ممکن است متفاوت باشد. مستندات والکس را بررسی کنید.
    # فرمت‌های رایج: {'Authorization': f'Bearer {api_key}'} یا {'X-Api-Key': api_key}
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # ارسال درخواست GET به سرور والکس
        response = requests.get(url, headers=headers)
        
        # بررسی موفقیت‌آمیز بودن درخواست
        response.raise_for_status()  # اگر کد وضعیت خطا باشد (مثل 401, 403, 404)، یک استثنا ایجاد می‌کند
        
        # بازگرداندن داده‌ها در فرمت JSON
        return response.json()
        
    except requests.exceptions.HTTPError as http_err:
        print(f"خطای HTTP رخ داد: {http_err}")
        print(f"متن پاسخ سرور: {response.text}")
        return None
    except Exception as err:
        # سایر خطاها (مثل مشکلات شبکه)
        print(f"خطای دیگری رخ داد: {err}")
        return None
      
def get_specific_crypto_data():
    """
    این تابع منطق اصلی را در خود دارد:
    1. لیست ارزهای هدف را از settings می‌خواند.
    2. داده‌ها را از API والکس دریافت می‌کند.
    3. داده‌ها را بر اساس لیست ارزها فیلتر می‌کند.
    4. یک دیکشنری حاوی داده‌های فیلتر شده یا یک دیکشنری خطا را برمی‌گرداند.
    """
    target_symbols = settings.TARGET_CRYPTO_SYMBOLS
    
    api_response = get_all_markets_data()
    
    if not api_response:
        return {"error": "امکان دریافت اطلاعات از سرور والکس وجود ندارد."}
    
    all_markets_data = api_response.get('result', {}).get('symbols', {})
    
    if not all_markets_data:
        return {"error": "ساختار پاسخ از API والکس تغییر کرده یا خالی است."}

    filtered_data = {
        market_name: market_info 
        for market_name, market_info in all_markets_data.items() 
        if (
            market_info.get('baseAsset', '').upper() in target_symbols and
            market_info.get('quoteAsset', '').upper() == 'TMN'
        )
    }
    
    if not filtered_data:
         return {"message": "هیچ‌کدام از ارزهای تعریف شده در لیست شما با واحد تومان یافت نشدند.", "target_symbols": target_symbols}
    
    return filtered_data