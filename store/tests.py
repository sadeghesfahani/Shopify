from django.test import TestCase
from django.test.client import Client
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.utils import json

from .product import Product
from .category import Category
from .views import ProductAPI
from .store import Store
from .Users import Admin
from account.users import BaseUserModel, UserDataStructure


class TestUrl(TestCase):
    def __init__(self, Object):
        self.request = APIRequestFactory().get("")
        self.product = Product(self.request)
        self.category = Category(self.request)
        self.store = Store(self.request)
        self.admin = Admin(self.request)

        super(TestUrl, self).__init__(Object)

    def testProductListURL(self):
        product_list = ProductAPI.as_view({"get": "list"})
        response = product_list(self.request)
        self.assertEqual(response.status_code, 200)

    def testProductRetrieveURL(self):
        product_detail = ProductAPI.as_view({"get": "retrieve"})
        new_category = self.category.addNew({'name': "first_category", "parent": None})
        new_admin = BaseUserModel.register(
            UserDataStructure(first_name="admin", last_name="admin", email="admin@gmail.com",
                              password="jshkfjsjhfgshjgfjh"))
        new_store = self.store.addStore(name="store1", description="something", admins=new_admin)
        new_product = self.product.addNew(
            {"name": "something", "description": "something", "category": new_category, "store": new_store,
             "price": 50000})
        response = product_detail(self.request, pk=new_product.id)
        self.assertEqual(response.data['name'], 'something')
        self.assertEqual(response.data['description'], 'something')
        self.assertEqual(response.data['price'], 50000)
        self.assertEqual(response.data['category'], new_category.id)
        self.assertEqual(response.data['store'], new_store.id)
        self.assertEqual(response.status_code, 200)
        response = product_detail(self.request, pk=12)
        self.assertEqual(response.status_code, 404)

    def testCreateAPIURL(self):
        new_category = self.category.addNew({'name': "first_category", "parent": None})
        new_admin = BaseUserModel.register(
            UserDataStructure(first_name="admin", last_name="admin", email="admin@gmail.com",
                              password="jshkfjsjhfgshjgfjh"))
        new_store = self.store.addStore(name="store1", description="something", admins=new_admin)

        json_data = json.dumps(
            {"name": "something", "description": "something", "category": new_category.id,
             "price": 50000})
        response = self.client.post(reverse('product-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)
        self.client.login(username="admin@gmail.com", password="jshkfjsjhfgshjgfjh")
        response = self.client.post(reverse('product-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product.selectById(response.data['id']).name)

        json_data = json.dumps(
            {"name": "something",
             "description": "something",
             "category": new_category.id,
             "price": 50000,
             "attributes": [
                 {
                     "options": [
                         {
                             "name": "3.2 Mhzzz",
                             "type": 0,
                             "price": 0,
                         },
                         {
                             "name": "ajabz",
                             "type": 0,
                             "price": 0,
                         }
                     ],
                     "name": "CPU",
                 },
                 {
                     "options": [
                         {
                             "name": "16inc",
                             "type": 0,
                             "price": 0
                         }
                     ],
                     "name": "صفحه نمایش"
                 }
             ]})
        response = self.client.post(reverse('product-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.data['attributes'][0]['name'], "CPU")
        self.assertEqual(response.data['attributes'][1]['name'], "صفحه نمایش")
        self.assertEqual(response.data['attributes'][0]['options'][1]['name'], "ajabz")

    def testModifyAPIURL(self):
        new_category = self.category.addNew({'name': "first_category", "parent": None})
        new_admin = BaseUserModel.register(
            UserDataStructure(first_name="admin", last_name="admin", email="admin@gmail.com",
                              password="jshkfjsjhfgshjgfjh"))
        new_store = self.store.addStore(name="store1", description="something", admins=new_admin)

        json_data = json.dumps(
            {"name": "something", "description": "something", "category": new_category.id,
             "price": 50000})
        self.client.login(username="admin@gmail.com", password="jshkfjsjhfgshjgfjh")
        response = self.client.post(reverse('product-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        product_id = response.data['id']
        response = self.client.get(reverse('product-detail', args=(product_id,)))
        self.assertEqual(response.data['name'], "something")
        json_data = json.dumps(
            {"name": "somethingelse", "description": "somethingelse", "category": new_category.id,
             "price": 10000})

        response = self.client.put(reverse('product-detail', args=(product_id,)), json_data,
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.data['name'], "somethingelse")
        self.assertEqual(response.data['description'], "somethingelse")
        self.assertEqual(response.data['price'], 10000)

        json_data = json.dumps(
            {"name": "something",
             "description": "something",
             "category": new_category.id,
             "price": 50000,
             "attributes": [
                 {
                     "options": [
                         {
                             "name": "3.2 Mhzzz",
                             "type": 0,
                             "price": 0,
                         },
                         {
                             "name": "ajabz",
                             "type": 0,
                             "price": 0,
                         }
                     ],
                     "name": "CPU"
                 },
                 {
                     "options": [
                         {
                             "name": "16inc",
                             "type": 0,
                             "price": 0
                         }
                     ],
                     "name": "صفحه نمایش"
                 }
             ]})
        response = self.client.post(reverse('product-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        product_id = response.data['id']

        json_data = json.dumps(
            {"name": "somethingelse",
             "description": "somethingelse",
             "category": new_category.id,
             "price": 60000,
             "attributes": [
                 {
                     "options": [
                         {
                             "name": "changed",
                             "type": 1,
                             "price": 10,
                         },
                         {
                             "name": "yes it changed",
                             "type": 1,
                             "price": 10,
                         }
                     ],
                     "name": "CPU-changed",
                 },
                 {
                     "options": [
                         {
                             "name": "16inc-changed",
                             "type": 1,
                             "price": 5
                         }
                     ],
                     "name": "changgggg"
                 }
             ]})
        response = self.client.put(reverse('product-detail', args=(product_id,)), json_data,
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.data['attributes'][0]['name'], "CPU-changed")
        self.assertEqual(response.data['attributes'][1]['name'], "changgggg")
        self.assertEqual(response.data['attributes'][0]['options'][1]['name'], "yes it changed")

        json_data = json.dumps(
            {"name": "somethingelse",
             "description": "somethingelse",
             "category": new_category.id,
             "price": 60000,
             "attributes": [
                 {
                     "id": 5,
                     "options": [
                         {
                             "name": "changed",
                             "type": 1,
                             "price": 10,
                         },
                         {
                             "name": "yes it changed",
                             "type": 1,
                             "price": 10,
                         }
                     ],
                     "name": "CPU-changed",
                 },
                 {
                     "options": [
                         {
                             "name": "16inc-changed",
                             "type": 1,
                             "price": 5
                         }
                     ],
                     "name": "changgggg"
                 }
             ]})

        response = self.client.put(reverse('product-detail', args=(product_id,)), json_data,
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 404)

    def testCreateCategoryURL(self):
        json_data = json.dumps({'name': "root1"})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.data['name'], 'root1')
        json_data = json.dumps({'name': "root2"})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.data['name'], 'root2')
        json_data = json.dumps({'name': "child1 of root1", "parent": 1})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        category = Category()
        parent_id = category.selectById(response.data['id']).parent.id
        self.assertEqual(response.data['parent'], parent_id)

        self.assertEqual(category.getChildren(parent_id)[0].id, response.data['id'])
        self.assertEqual(response.data['name'], 'child1 of root1')

    def testModifyCategoryURL(self):
        json_data = json.dumps({'name': "root1"})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        categpry_id = response.data['id']
        json_data = json.dumps({'name': "root1-modified", 'shown_in_menu_bar': False})
        response = self.client.put(reverse('category-detail', args=(categpry_id,)), json_data,
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.data['shown_in_menu_bar'], False)
        self.assertEqual(response.data['name'], "root1-modified")
        json_data = json.dumps({'name': "root2"})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        second_parent = response.data['id']
        json_data = json.dumps({'name': "sub1",'parent': categpry_id})
        response = self.client.post(reverse('category-list'), json_data, content_type='application/json',
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        category_id = response.data['id']
        print(response.data)
        json_data = json.dumps({'name': "root1-modified", 'shown_in_menu_bar': False,'parent':second_parent })
        response = self.client.put(reverse('category-detail', args=(category_id,)), json_data,
                                   content_type='application/json',
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.data['name'],'root1-modified')
        self.assertEqual(response.data['shown_in_menu_bar'],False)
        self.assertEqual(response.data['parent'],second_parent)
        print(response.data)