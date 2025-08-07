# Create your views here.
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import get_all_markets_data , get_specific_crypto_data 

class MarketStatsView(APIView):
    """
    یک View برای نمایش اطلاعات کلی بازارها.
    همچنین می‌تواند اطلاعات ارزهای خاصی را فیلتر و نمایش دهد.
    """
    def get(self, request, *args, **kwargs):
        # دریافت پارامتر 'symbols' از کوئری استرینگ URL
        # مثال: /api/market-stats/?symbols=BTC,ETH
        symbols_query = request.query_params.get('symbols', None)
        
        # فراخوانی سرویس برای دریافت تمام داده‌های بازار
        api_response = get_all_markets_data()
        
        if not api_response:
            return Response(
                {"error": "امکان دریافت اطلاعات از سرور والکس وجود ندارد."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
            
        # --- اصلاح کلیدی ---
        # دسترسی به دیکشنری بازارها بر اساس ساختار صحیح API والکس
        # داده‌ها داخل کلید 'result' و سپس 'symbols' قرار دارند
        all_markets_data = api_response.get('result', {}).get('symbols', {})
        
        if not all_markets_data:
             return Response(
                {"error": "ساختار پاسخ از API والکس تغییر کرده یا خالی است.", "raw_response": api_response},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if symbols_query:
            # اگر کاربر نمادهای خاصی را درخواست کرده بود
            # تبدیل رشته ورودی به یک لیست از نمادها با حروف بزرگ
            # مثال: "btc, eth" -> ['BTC', 'ETH']
            requested_symbols = [s.strip().upper() for s in symbols_query.split(',')]
            
            # فیلتر کردن نتایج
            # ما در میان تمام بازارها (مثل 'BTC-TMN', 'ETH-USDT') می‌گردیم
            # و بازارهایی را انتخاب می‌کنیم که ارز پایه (baseAsset) آن‌ها در لیست ما باشد.
            filtered_data = {
                market_name: market_info 
                for market_name, market_info in all_markets_data.items() 
                if market_info.get('baseAsset', '').upper() in requested_symbols
            }
            
            if not filtered_data:
                 return Response(
                    {"message": "هیچ‌کدام از ارزهای درخواستی در بازارهای والکس یافت نشدند.", "requested_symbols": requested_symbols},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            return Response(filtered_data, status=status.HTTP_200_OK)
        
        # اگر هیچ نمادی مشخص نشده بود، تمام اطلاعات بازارها را برگردان
        return Response(all_markets_data, status=status.HTTP_200_OK)

class SpecificCryptoStatsView(APIView):
    """
    این View با فراخوانی سرویس، اطلاعات بازارهای مربوط به لیست ارزهای
    تعریف شده در settings.py را برمی‌گرداند.
    """
    def get(self, request, *args, **kwargs):
        # فراخوانی تابع منطقی مشترک
        data = get_specific_crypto_data()
        
        # اگر تابع خطا برگردانده بود، آن را با کد وضعیت مناسب نمایش بده
        if 'error' in data:
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if 'message' in data and not any(isinstance(v, dict) for v in data.values()):
             return Response(data, status=status.HTTP_404_NOT_FOUND)

        # در غیر این صورت، داده‌های موفقیت‌آمیز را برگردان
        return Response(data, status=status.HTTP_200_OK)