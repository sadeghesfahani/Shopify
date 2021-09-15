from django.test import TestCase
from django.test.client import Client
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from .market import Market
from .product import Product
from .category import Category, CategoryDataStructure
from .views import ProductAPI
from .store import Store
from .Users import Admin
from account.users import BaseUserModel, UserDataStructure


class TestUrl(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.customer = dict()
        self.user_store_admin_2 = dict()
        self.user_store_admin_1 = dict()
        self.user1_store_admin = dict()
        self.user_admin = dict()

    def setUp(self) -> None:
        password = 'adminadminadmin'
        store = Store()
        category = Category()
        user_admin = UserDataStructure(first_name='admin', last_name='admin', email='admin@gmail.com',
                                       password=password, user_type=0)
        user_store_admin_1 = UserDataStructure(first_name='admin1', last_name='admin', email='admin1@gmail.com',
                                               password=password, user_type=1)
        user_store_admin_2 = UserDataStructure(first_name='admin2', last_name='admin', email='admin2@gmail.com',
                                               password=password, user_type=1)
        customer = UserDataStructure(first_name='customer', last_name='customer', email='customer@gmail.com',
                                     password=password, user_type=3)

        self.user_admin['user'] = BaseUserModel.register(user_admin)
        self.user_admin['token'] = BaseUserModel.getToken(self.user_admin['user'])
        self.user_store_admin_1['user'] = BaseUserModel.register(user_store_admin_1)
        self.user_store_admin_1['token'] = BaseUserModel.getToken(self.user_store_admin_1['user'])
        self.user_store_admin_2['user'] = BaseUserModel.register(user_store_admin_2)
        self.user_store_admin_2['token'] = BaseUserModel.getToken(self.user_store_admin_2['user'])
        self.customer['user'] = BaseUserModel.register(customer)
        self.customer['token'] = BaseUserModel.getToken(self.customer['user'])

        self.main_store = store.addStore(name='main',
                                         description='Main store',
                                         admins=self.user_admin['user'])
        self.store_1 = store.addStore(name='store1',
                                      description='store1',
                                      admins=self.user_store_admin_1['user'])
        self.store_2 = store.addStore(name='store2',
                                      description='store2',
                                      admins=self.user_store_admin_2['user'])
        # root_category_1 = CategoryDataStructure(name='root1', shown_in_menu_bar=True)
        # root_category_2 = CategoryDataStructure(name='root2', shown_in_menu_bar=True)
        self.root_category_1 = category.addNew({"name": 'root1', "shown_in_menu_bar": True})
        self.root_category_2 = category.addNew({"name": 'root2', "shown_in_menu_bar": True})

        self.child_category_2_1 = category.addNew(
            {"name": 'root1', "shown_in_menu_bar": True, "parent": self.root_category_1})

        self.child_child_category_2_1_1 = category.addNew({"name": 'root1',  "shown_in_menu_bar":True, "parent":self.child_category_2_1})

    def PrepareHeader(self, token):
        return {"Authorization": f"token {token}"}

    def testPermissions(self):
        self.assertEqual(0, 0)
