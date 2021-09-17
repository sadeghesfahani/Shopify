from store.market_manager import BaseMarketObjectManager
from .models import Discount as DiscountModel


class Discount(BaseMarketObjectManager):
    targetObject = DiscountModel
