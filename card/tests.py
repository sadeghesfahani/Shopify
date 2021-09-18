import datetime

from django.test import TestCase

from store.test_base.marketBase import TestBase
from .card import *


# Create your tests here.


class TestCard(TestBase):
    def setUp(self) -> None:
        self.card_object = Card()
        self.order_object = Order()
        self.delivery_object = Delivery()
        self.additional_option_object = AdditionalOption()
        self.discount = Discount()
        super(TestCard, self).setUp()

    def testCreation(self):
        order1 = self.order_object.addNew(self.product_1, 3)
        order2 = self.order_object.addNew(self.product_1, 2)
        order3 = self.order_object.addNew(self.product_1, 5)
        delivery1 = self.delivery_object.addNew('peyk', 5000)
        option = self.additional_option_object.addNew('arzesh afzude', 'baraye sherkat ha', 0, 8)
        address1 = BaseUserModel().addAddress(self.customer['user'], '734653659723', 'tehran shahriar')
        address2 = BaseUserModel().addAddress(self.customer['user'], '23424234', 'khodasan shahriar')
        discount1 = self.discount.addNew('cupon', 5, 2, None, 50,
                                         datetime.datetime.now() + datetime.timedelta(days=7, hours=0, minutes=0,
                                                                                      seconds=0))
        card = self.card_object.addNew(self.customer['user'], delivery=delivery1, receive_time=datetime.datetime.now(),
                                       address_good=address1, address_invoice=address2, discount=discount1,
                                       additional_option=option)
        self.card_object.addOrderToCard(card, order1)
        self.card_object.addOrderToCard(card, order2)
        self.card_object.addOrderToCard(card, order3)
        self.assertEqual(card.total_cost, 56300)

        option = self.additional_option_object.addNew('arzesh afzude', 'baraye sherkat ha', 1, 5000)
        card = self.card_object.addNew(self.customer['user'], delivery=delivery1, receive_time=datetime.datetime.now(),
                                       address_good=address1, address_invoice=address2, discount=discount1,
                                       additional_option=option)
        self.card_object.addOrderToCard(card, order1)
        self.card_object.addOrderToCard(card, order2)
        self.card_object.addOrderToCard(card, order3)
        self.assertEqual(card.total_cost, 57500)
