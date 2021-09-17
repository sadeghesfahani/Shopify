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
        super(TestCard, self).setUp()

    def testCreation(self):
        order1 = self.order_object.addNew(self.product_1, 3)
        order2 = self.order_object.addNew(self.product_1, 2)
        order3 = self.order_object.addNew(self.product_1, 5)
        delivery1 = self.delivery_object.addNew('peyk', 5000)
        option = self.additional_option_object.addNew('arzesh afzude', 'baraye sherkat ha', 0, 8)
        self.card_object.addNew(self.customer,delivery1,)
