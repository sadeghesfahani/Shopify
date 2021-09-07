from .models import *
from django.shortcuts import get_object_or_404


class StoreObj:
    category_class = Category
    product_class = Product
    store_class = Store

    def __init__(self):
        self.product = Product()
        self.category = Category()


class Product:

    def __init__(self):
        self.query_set = dict()
        self.order_by = str()
        self.limits = list()

    @staticmethod
    def selectById(product_id):
        return StoreObj.product_class.objects.get(id=product_id)

    def category(self, category_id):
        self.query_set['category_id'] = category_id
        return self

    def store(self, store_id):
        self.query_set['store_id'] = store_id
        return self

    def orderBy(self, order_by):
        self.order_by = order_by
        return self

    def limitsBy(self, low, high):
        self.limits = [low, high]
        return self

    def fetch(self):
        query_set = StoreObj.product_class.objects.filter(**self.query_set).order_by(
            self.order_by) if self.order_by else StoreObj.product_class.objects.filter(**self.query_set)

        return query_set[self.limits[0]:self.limits[1]] if self.limits else query_set

    @staticmethod
    def addProduct(product_data_structure):
        return StoreObj.product_class(**product_data_structure.__dict__)

    @staticmethod
    def editProduct(product_data_structure, product_id):
        return StoreObj.product_class.objects.get(pk=product_id).update(**product_data_structure.__dict__)


class Category:

    def addCategory(self, category_data_structure):
        category = StoreObj.category_class(**category_data_structure.__dict__)
        category.save()
        return category

    @staticmethod
    def selectById(category_id):
        return StoreObj.category_class.objects.get(pk=category_id)


class ProductDataStructure:
    def __init__(self, name, category, description, store):
        self.name = name
        self.category = category
        self.description = description
        self.store = store


class CategoryDataStructure:
    store = StoreObj()

    def __init__(self, name, parent=None, **kwargs):
        self.name = name
        self.parent = None if parent is None else CategoryDataStructure.store.category.selectById(parent)
        # self.parent = CategoryDataStructure.store.category.selectById(parent)
