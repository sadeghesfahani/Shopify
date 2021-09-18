from django.contrib.auth import get_user_model

from shopify_first_try.utils import getObject
from store.market_manager import BaseMarketObjectManager
from .errors import handleError
from .models import Discount as DiscountModel

User = get_user_model()


class Discount(BaseMarketObjectManager):
    targetObject = DiscountModel

    def addNew(self, name, discount, discount_type, users=None, limits=None, expire=None):
        structured_discount_data = DiscountDataStructure(name, discount, discount_type, users, limits, expire)
        users_to_add = structured_discount_data.users
        del structured_discount_data.users
        newly_added_discount = self.targetObject(**structured_discount_data.__dict__)
        newly_added_discount.save()
        if isinstance(users_to_add,list):
            for user in users_to_add:
                newly_added_discount.users.add(user)
        else:
            newly_added_discount.users.add(users_to_add)
        newly_added_discount.save()
        return newly_added_discount


class DiscountDataStructure:
    def __init__(self, name, discount, discount_type, users=None, limits=None, expire=None):
        self.name = name
        self.discount = discount
        self.discount_type = self.validatedDiscountType(discount_type)
        self.users = self.handleUsers(users)
        self.limits = limits
        self.expire = expire

    @staticmethod
    @handleError(Discount())
    def validatedDiscountType(discount_type):
        if 1 <= discount_type <= 2:
            return discount_type
        else:
            raise ValueError

    @staticmethod
    @handleError(User)
    def handleUsers(users):
        users_list = list()
        if isinstance(users, list):
            for user in users:
                user_object = getObject(User, user)
                users_list.append(user_object)
        else:
            user_object = getObject(User, users)
            return user_object
        return users_list
