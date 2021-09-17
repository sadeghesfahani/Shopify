from store.market_manager import BaseMarketObjectManager
from .models import Discount as DiscountModel


class Discount(BaseMarketObjectManager):
    targetObject = DiscountModel

    def addNew(self, name, discount, discount_type, users=None, limits=None, expire=None):
        pass