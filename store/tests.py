from django.test import TestCase
from django.test.client import Client
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APIClient
from rest_framework.utils import json

from .market import Market
from .product import Product
from .category import Category, CategoryDataStructure
from .serializers import CategorySerializer, CustomCategorySerializer
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
        # CategoryDataStructure(name='dummy')
        self.dummy_category = json.dumps({"name": "something"})
        self.dummy_category_changed = json.dumps({"name": "changed", "parent": 2, "shown_in_menu_bar": False})

    def sendPostRequest(self, url, data):
        return self.client.post(reverse(url), **RequestDataStructure(data).__dict__)

    def sendPostRequestWithUser(self, user, url, data):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token ' + user['token'])
        return client.post(reverse(url), **RequestDataStructure(data).__dict__)

    def sendPutRequestWithUserWithPk(self, user, url, data, pk):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='token ' + user['token'])
        return client.put(reverse(url, args=(pk,)), **RequestDataStructure(data).__dict__)

    def testCategory(self):
        # permissions
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        response = self.sendPostRequest('category-list', self.dummy_category)
        self.assertEqual(response.status_code, 401)
        response = self.sendPostRequestWithUser(self.user_store_admin_2, 'category-list', self.dummy_category)
        self.assertEqual(response.status_code, 403)

        # creation
        response = self.sendPostRequestWithUser(self.user_admin, 'category-list', self.dummy_category)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], json.loads(self.dummy_category)['name'])
        category_id_created_by_user_admin = response.data['id']

        # modify
        response = self.sendPutRequestWithUserWithPk(self.user_store_admin_2, 'category-detail', self.dummy_category,
                                                     category_id_created_by_user_admin)
        self.assertEqual(response.status_code, 403)
        response = self.sendPutRequestWithUserWithPk(self.user_admin, 'category-detail', self.dummy_category_changed,
                                                     category_id_created_by_user_admin)
        self.assertEqual(response.data['id'], category_id_created_by_user_admin)
        self.assertEqual(response.data['name'], json.loads(self.dummy_category_changed)['name'])
        self.assertEqual(response.data['parent'], json.loads(self.dummy_category_changed)['parent'])


# data structures
class RequestDataStructure:
    def __init__(self, data, content_type='application/json', HTTP_X_REQUESTED_WITH='XMLHttpRequest'):
        self.data = data
        self.content_type = content_type
        self.HTTP_X_REQUESTED_WITH = HTTP_X_REQUESTED_WITH
