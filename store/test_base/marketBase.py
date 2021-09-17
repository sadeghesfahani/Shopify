import json
from django.test import TestCase

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from account.users import BaseUserModel, UserDataStructure
from store.category import Category
from store.product import Product
from store.store import Store


class TestBase(TestCase):
    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.customer = dict()
        self.user_store_admin_2 = dict()
        self.user_store_admin_1 = dict()
        self.user1_store_admin = dict()
        self.user_admin = dict()

    def setUp(self) -> None:
        password = 'this is gonna be a dummy password'
        store = Store()
        category = Category()
        product = Product()
        user_admin = UserDataStructure(first_name='admin', last_name='admin', email='admin@gmail.com',
                                       password=password, user_type=1)
        user_store_admin_1 = UserDataStructure(first_name='admin1', last_name='admin', email='admin1@gmail.com',
                                               password=password, user_type=2)
        user_store_admin_2 = UserDataStructure(first_name='admin2', last_name='admin', email='admin2@gmail.com',
                                               password=password, user_type=2)
        customer = UserDataStructure(first_name='customer', last_name='customer', email='customer@gmail.com',
                                     password=password, user_type=0)

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
        self.root_category_1 = category.addNew({"name": 'root1', "shown_in_menu_bar": True})
        self.root_category_2 = category.addNew({"name": 'root2', "shown_in_menu_bar": True})

        self.child_category_2_1 = category.addNew(
            {"name": 'root1', "shown_in_menu_bar": True, "parent": self.root_category_1})

        self.child_child_category_2_1_1 = category.addNew(
            {"name": 'root1', "shown_in_menu_bar": True, "parent": self.child_category_2_1})
        self.dummy_category = json.dumps({"name": "something"})
        self.dummy_category_changed = json.dumps({"name": "changed", "parent": 2, "shown_in_menu_bar": False})

        self.product_1 = product.addNew(
            {'name': 'product1', 'description': 'product1', 'price': 5000, 'store': self.store_2,
             "category": self.root_category_1})

        self.product_dummy_data = {'name': 'dummy product', 'description': 'dummy product', 'price': 54654564,
                                   'store': self.store_2,
                                   "category": self.root_category_1}
        self.product_dummy_data_json = json.dumps(
            {"name": "dummy product", "description": "dummy product", "price": 54654564,
             "store": self.store_2.id,
             "category": self.root_category_1.id})
        self.product_dummy_data_json_without_store = json.dumps(
            {"name": "dummy product", "description": "dummy product", "price": 54654564,
             "category": self.root_category_1.id})
        self.product_dummy_data_json_without_store_without_name = json.dumps(
            {"description": "dummy product", "price": 54654564,
             "category": self.root_category_1.id})

    def sendPostRequest(self, url, data):
        return self.client.post(reverse(url), **RequestDataStructure(data).__dict__)

    @staticmethod
    def sendPostRequestWithUser(user, url, data):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token ' + user['token'])
        return client.post(reverse(url), **RequestDataStructure(data).__dict__)

    @staticmethod
    def sendPutRequestWithUserWithPk(user, url, data, pk):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token ' + user['token'])
        return client.put(reverse(url, args=(pk,)), **RequestDataStructure(data).__dict__)

    @staticmethod
    def sendGetWithPk(url, pk):
        client = APIClient()
        return client.get(reverse(url, args=(pk,)))


# data structures
class RequestDataStructure:
    def __init__(self, data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest'):
        self.data = data
        self.content_type = content_type
        self.HTTP_X_REQUESTED_WITH = HTTP_X_REQUESTED_WITH
