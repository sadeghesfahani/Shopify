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


