from rest_framework.reverse import reverse
from rest_framework.utils import json
from store.test_base.marketBase import TestBase


class TestUrl(TestBase):

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

    def testProduct(self):
        # permissions
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('product-detail', args=(self.product_1.id,)))
        self.assertEqual(response.status_code, 200)

        response = self.sendPostRequestWithUser(user=self.customer, url='product-list', data=self.product_dummy_data)
        self.assertEqual(response.status_code, 403)

        # user_store_admin_1 is admin of store 1
        # user_store_admin_2 is admin of store 2
        # product_dummy_data is store 2
        response = self.sendPostRequestWithUser(user=self.user_store_admin_1, url='product-list',
                                                data=self.product_dummy_data_json)
        self.assertEqual(response.status_code, 403)
        response = self.sendPostRequestWithUser(user=self.user_store_admin_2, url='product-list',
                                                data=self.product_dummy_data_json)
        self.assertEqual(response.status_code, 200)
        # admin permission

        response = self.sendPostRequestWithUser(user=self.user_admin, url='product-list',
                                                data=self.product_dummy_data_json)
        self.assertEqual(response.status_code, 200)

        response = self.sendPostRequestWithUser(user=self.user_store_admin_2, url='product-list',
                                                data=self.product_dummy_data_json_without_store)
        print(response.data)
        self.assertEqual(response.status_code, 200)
