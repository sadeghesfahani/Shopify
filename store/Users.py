from .market_manager import BaseMarketObjectManager
from django.contrib.auth import get_user_model

User = get_user_model()


class Customer(BaseMarketObjectManager):
    targetObject = get_user_model()

    def __init__(self, request):
        super(Customer, self).__init__(request)
        self.querySet = {'TYPES': User.CUSTOMER}

    def currentUser(self):
        return self.selectById(self.request.user.id)


class Admin(BaseMarketObjectManager):
    targetObject = get_user_model()

    def __init__(self, request):
        super(Admin, self).__init__(request)
        self.querySet = {'TYPES': User.DEPARTMENT_ADMIN}

    def currentUser(self):
        return self.selectById(self.request.user.id) if self.request.user.is_authenticated else None

    def getStore(self):
        return self.currentUser().admins.get()
