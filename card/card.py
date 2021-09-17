from account.users import BaseUserModel
from store.errors import handleError
from store.market import Market
from store.discount import Discount
from store.product import Option
from .models import Order as OrderModel, Card as CardModel


class Card:
    targetObject = CardModel

    def addNew(self):
        pass


class Order:
    targetObject = OrderModel

    @handleError(targetObject)
    def selectById(self, order_id):
        return self.targetObject.objects.get(pk=order_id)

    def addNew(self, product, product_option, quantity, user):
        order_structured_data = OrderDataStructure(product, product_option, quantity, user)
        newly_added_order = self.targetObject(**order_structured_data.__dict__)
        newly_added_order.save()
        return newly_added_order


class OrderDataStructure:
    def __init__(self, product, product_option, quantity):
        option = Option()
        market = Market()
        if isinstance(product, int) or isinstance(product, str):
            self.product = market.product.selectById(product)
        else:
            self.product = product

        if isinstance(product_option, int) or isinstance(product_option, str):
            self.option = option.selectById(product_option)
        else:
            self.option = option
        self.count = quantity


class CardDataStructure:
    def __init__(self, user, discount):
        discount_object = Discount()
        if isinstance(user, int) or isinstance(user, str):
            try:
                user_id = int(user)
                self.user = BaseUserModel().getUserById(user_id)
            except ValueError:
                token = str(user)
                self.user = BaseUserModel().getUserByToken(token)
        else:
            self.user = user
        if isinstance(discount, int) or isinstance(discount, str):
            self.discount = discount_object.selectById(discount)
        else:
            self.discount = discount
