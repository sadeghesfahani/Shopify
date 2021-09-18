import datetime

from django.test import TestCase

from store.product import Attribute, AttributeDataStructure, OptionDataStructure
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

        attribute1 = AttributeDataStructure(name='attribute1', product=self.product_1)
        self.product_attribute = Attribute().addNewAttribute(self.product_1.id, attribute1)
        option1 = OptionDataStructure(name='option 1', attribute=self.product_attribute, type=1, price=4000)
        self.option_product = Option().addNewOption(self.product_attribute.id, option1)

        order4 = self.order_object.addNew(self.product_1, 5, self.option_product)

        card1 = self.card_object.addNew(self.customer['user'], delivery=delivery1, receive_time=datetime.datetime.now(),
                                       address_good=address1, address_invoice=address2, discount=discount1,
                                       additional_option=option)
        self.card_object.addOrderToCard(card1, order1)
        self.card_object.addOrderToCard(card1, order2)
        self.card_object.addOrderToCard(card1, order3)
        self.card_object.addOrderToCard(card1, order4)
        self.assertEqual(card1.total_cost,76500)

        option2 = OptionDataStructure(name='option 1', attribute=self.product_attribute, type=2, price=4000)
        self.option_product1 = Option().addNewOption(self.product_attribute.id, option2)
        order5 = self.order_object.addNew(self.product_1, 5, self.option_product1)
        card2 = self.card_object.addNew(self.customer['user'], delivery=delivery1, receive_time=datetime.datetime.now(),
                                       address_good=address1, address_invoice=address2, discount=discount1,
                                       additional_option=option)

        self.card_object.addOrderToCard(card2, order1)
        self.card_object.addOrderToCard(card2, order2)
        self.card_object.addOrderToCard(card2, order3)
        self.card_object.addOrderToCard(card2, order4)
        self.card_object.addOrderToCard(card2, order5)
        self.assertEqual(card2.total_cost,119250)
        print(card2.total_cost)

        option3 = OptionDataStructure(name='option 1', attribute=self.product_attribute, type=3, price=15)
        self.option_product2 = Option().addNewOption(self.product_attribute.id, option3)
        order6 = self.order_object.addNew(self.product_1, 5, self.option_product2)
        card3 = self.card_object.addNew(self.customer['user'], delivery=delivery1, receive_time=datetime.datetime.now(),
                                        address_good=address1, address_invoice=address2, discount=discount1,
                                        additional_option=option)

        self.card_object.addOrderToCard(card3, order1)
        self.card_object.addOrderToCard(card3, order2)
        self.card_object.addOrderToCard(card3, order3)
        self.card_object.addOrderToCard(card3, order4)
        self.card_object.addOrderToCard(card3, order5)
        self.card_object.addOrderToCard(card3, order5)
        self.card_object.addOrderToCard(card3, order6)

        self.assertEqual(card3.total_cost,146562.5)