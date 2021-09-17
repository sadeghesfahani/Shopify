from django.test import TestCase

from store.test_base.marketBase import TestBase
from .card import *


# Create your tests here.


class TestCard(TestBase):
    def setUp(self) -> None:
        self.card_object = Card()
        self.order_object = Order()
        super(TestCard, self).setUp()

    def testCreation(self):
        order1 = self.order_object.addNew(self.product_1, 3)
        order2 = self.order_object.addNew(self.product_1, 2)
        order3 = self.order_object.addNew(self.product_1, 5)


