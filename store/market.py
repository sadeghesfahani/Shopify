from django.contrib.auth import get_user_model
from account.models import User
from store.models import Store as StoreModel, Product as ProductModel, Category as CategoryModel


class Market:
    """
    this class has been made to have full control over the business model and provide flexibility between separated
    models yet integrated business model, based on single responsibility principle and open-close principle, all classes
    build separately to have the least interaction with each other that may cause fragility during adding new features.
    """
    def __init__(self, request):
        self.product = Product(request)
        self.store = Store(request)
        self.customer = Customer(request)
        self.admin = Admin(request)
        self.category = Category(request)


class BaseMarketObjectManager:
    """
    this class provides the basic functionality will repetitively be using in Market subclasses
    all other objects will inherit the basic functionality
    """
    targetObject = None

    def __init__(self, request=None):
        self.querySet = dict()
        self.orderBy = False
        self.limits = None
        self.request = request

    @classmethod
    def selectById(cls, identifier):
        return cls.targetObject.objects.get(id=identifier)

    def orderBy(self, order_by_string):
        self.orderBy = order_by_string
        return self

    def limitsBy(self, lower_boundary_band, higher_boundary_band):
        self.limits = [lower_boundary_band, higher_boundary_band]
        return self

    @classmethod
    def getClass(cls):
        return cls

    def fetch(self):
        objects = self.getClass().targetObject.objects.filter(**self.querySet).order_by(
            self.orderBy) if self.orderBy else self.getClass().targetObject.objects.filter(**self.querySet)
        return objects[self.limits[0]:self.limits[1]] if self.limits else objects


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
        return self.currentUser().store_set.get()


class Store(BaseMarketObjectManager):
    targetObject = StoreModel

    def currentStore(self):
        return self.targetObject.objects.get(admins__in=self.request.user)

    def addStoreDataStructure(self, **kwargs):
        return StoreDataStructure(self.request, **kwargs)

    def addStore(self, **kwargs):
        return self.targetObject(**self.addStoreDataStructure(self.request, **kwargs).__dict__)

    def modifyStore(self, store_object_or_id, **kwargs):
        if isinstance(store_object_or_id, int):
            modifying_store = self.targetObject.objects.get(id=store_object_or_id)
        else:
            modifying_store = store_object_or_id
        modifying_store.update(**self.addStoreDataStructure(self.request, **kwargs).__dict__)

    def isAdminOfStore(self, store, user=None):
        store_to_check = self.getStore(store)
        user_to_check = self.getCurrentUser() if user is None else user
        return True if user_to_check in store_to_check.admins else False

    def getStore(self, store):
        return self.selectById(store) if isinstance(store, int) else store

    @staticmethod
    def getCurrentUser():
        admin_model = Admin()
        return admin_model.currentUser()


class Product(BaseMarketObjectManager):
    targetObject = ProductModel

    def filterByCategory(self, category_id):
        self.querySet["category_id"] = category_id
        return self

    def filterByStore(self, store_id):
        self.querySet['store_id'] = store_id
        return self

    def addNew(self, product_data):
        new_product = self.targetObject(**ProductDataStructure(self.request, **product_data).__dict__)
        new_product.save()
        return new_product

    def modify(self, product_id, product_data):
        product_to_modify = self.selectById(product_id)
        product_to_modify.__dict__.update(**ProductDataStructure(self.request, **product_data).__dict__)
        product_to_modify.save()
        return product_to_modify


class Category(BaseMarketObjectManager):
    targetObject = CategoryModel


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


class ProductDataStructure:
    """
    this data structure will always come into place to avoid and handle unexpected errors during transforming information
    """
    def __init__(self, request, name, category, description, store):
        market = Market(request)
        self.name = name
        if isinstance(category, int) or isinstance(category, str):
            self.category = market.category.selectById(category)
        else:
            self.category = category
        self.description = description
        if isinstance(store, int) or isinstance(store, str):
            self.store = market.store.selectById(store)
        else:
            self.store = store
        print(self.__dict__)
