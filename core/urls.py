from django.urls import path
from .views import MarketStatsView , SpecificCryptoStatsView

urlpatterns = [
    path('market-stats/', MarketStatsView.as_view(), name='market-stats'),
    path('specific-crypto-stats/', SpecificCryptoStatsView.as_view(), name='specific-crypto-stats'),
]