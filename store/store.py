from .market_manager import BaseMarketObjectManager
from .models import Store as StoreModel
from .Users import Admin


class Store(BaseMarketObjectManager):
    targetObject = StoreModel

    def currentStore(self):
        return self.targetObject.objects.get(admins__in=self.request.user)

    def addStoreDataStructure(self, **kwargs):
        return StoreDataStructure(self.request, **kwargs)

    def addStore(self, **kwargs):
        return self.targetObject(**self.addStoreDataStructure(**kwargs).__dict__)

    def modifyStore(self, store_object_or_id, **kwargs):
        if isinstance(store_object_or_id, int):
            modifying_store = self.targetObject.objects.get(id=store_object_or_id)
        else:
            modifying_store = store_object_or_id
        modifying_store.update(**self.addStoreDataStructure(**kwargs).__dict__)

    def isAdminOfStore(self, store, user=None):
        store_to_check = self.getStore(store)
        user_to_check = self.getCurrentUser() if user is None else user
        return True if user_to_check in store_to_check.admins else False

    def getStore(self, store):
        return self.selectById(store) if isinstance(store, int) else store

    def getCurrentUser(self):
        admin_model = Admin(self.request)
        return admin_model.currentUser()


class StoreDataStructure:
    """
    this data structure will always come into place to avoid and handle unexpected errors during transforming information
    """

    def __init__(self, request, name, description, admins=None):
        self.name = name
        self.description = description
        if admins is None:
            admin_object = Admin(request)
            admin = admin_object.currentUser()
            self.admins = [admin]
        else:
            if isinstance(admins, list):
                self.admins = admins
            else:
                self.admins = [admins]
