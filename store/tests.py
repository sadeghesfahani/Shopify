from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIRequestFactory
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
        print(response.data)
        self.assertEqual(response.data['name'], 'something')
        self.assertEqual(response.data['description'], 'something')
        self.assertEqual(response.data['price'], 50000)
        self.assertEqual(response.data['category'], new_category.id)
        self.assertEqual(response.data['store'], new_store.id)
        self.assertEqual(response.status_code, 200)
