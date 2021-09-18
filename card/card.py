from account.users import BaseUserModel
from shopify_first_try.utils import IsId, getObject
from store.errors import handleError
from store.market import Market
from store.discount import Discount
from store.market_manager import BaseMarketObjectManager
from store.product import Option
from .models import Order as OrderModel, Card as CardModel, AdditionalOption as AdditionalOptionModel, \
    Delivery as DeliveryModel


class Card:
    targetObject = CardModel

    def addNew(self, user, delivery, receive_time, address_good, discount=None, additional_option=None,
               address_invoice=None,
               payment_info=None, status=0):
        card_structured_data = CardDataStructure(user=user, discount=discount, additional_option=additional_option,
                                                 delivery=delivery,
                                                 receive_time=receive_time,
                                                 address_good=address_good,
                                                 address_invoice=address_invoice,
                                                 payment_info=payment_info,
                                                 status=status)
        newly_added_card = self.targetObject(**card_structured_data.__dict__)
        newly_added_card.save()
        return newly_added_card

    def addOrderToCard(self, card, orders):
        if IsId(card):
            card_object = self.selectById(card)
        else:
            card_object = card
        if isinstance(orders, list):
            for order in orders:
                order_to_add = getObject(Order(), order)
                card_object.orders.add(order_to_add)
        else:
            order_to_add = getObject(Order(), orders)
            card_object.orders.add(order_to_add)
        card_object.save()

    @handleError(targetObject)
    def selectById(self, card_id):
        return self.targetObject.objects.get(pk=card_id)

    @handleError(targetObject)
    def addPaymentInfo(self, card, info):
        card_object = getObject(self.targetObject, card)
        card_object.payment_info = info
        card_object.save()
        return card_object

    @handleError(targetObject)
    def changeStatus(self, card, status):
        if self.isStatusValid(status):
            card_object = getObject(self.targetObject, card)
            card_object.status = status
        else:
            raise ValueError

    @staticmethod
    def isStatusValid(status):
        return True if 0 <= status <= 4 else False


class Order:
    targetObject = OrderModel

    @handleError(targetObject)
    def selectById(self, order_id):
        return self.targetObject.objects.get(pk=order_id)

    def addNew(self, product, quantity, product_option=None):
        order_structured_data = OrderDataStructure(product, product_option, quantity)
        newly_added_order = self.targetObject(**order_structured_data.__dict__)
        newly_added_order.save()
        return newly_added_order


class OrderDataStructure:
    def __init__(self, product, product_option, quantity):
        option = Option()
        market = Market()
        self.product = getObject(market.product, product)
        self.option = getObject(option, product_option)
        self.count = quantity


class CardDataStructure:
    def __init__(self, user, discount, additional_option, delivery, receive_time, address_good, address_invoice=None,
                 payment_info=None, status=0):
        discount_object = Discount()
        additional_option_object = AdditionalOption()
        delivery_object = Delivery()
        if IsId(user):
            try:
                user_id = int(user)
                self.user = BaseUserModel().getUserById(user_id)
            except ValueError:
                token = str(user)
                self.user = BaseUserModel().getUserByToken(token)
        else:
            self.user = user

        self.discount = getObject(discount_object, discount)
        self.additional_option = getObject(additional_option_object, additional_option)
        self.delivery = getObject(delivery_object, delivery)
        self.receive_time = receive_time
        self.status = status
        self.address_to_send_good = address_good
        self.address_to_send_invoice = address_invoice
        self.payment_info = payment_info


class AdditionalOption(BaseMarketObjectManager):
    targetObject = AdditionalOptionModel

    def addNew(self, name, description, option_type, cost):
        newly_added_addtional_option = self.targetObject(name=name, description=description, option_type=option_type,
                                                         cost=cost)
        newly_added_addtional_option.save()
        return newly_added_addtional_option


class Delivery(BaseMarketObjectManager):
    targetObject = DeliveryModel

    def addNew(self, name, price):
        newly_added_delivery = self.targetObject(name=name, price=price)
        newly_added_delivery.save()
        return newly_added_delivery

