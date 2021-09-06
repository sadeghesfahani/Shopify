from .models import *
from django.shortcuts import get_object_or_404


class Store:
    category_class = Category
    product_class = Product

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
        return Store.product_class.objects.get(id=product_id)

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
        query_set = Store.product_class.objects.filter(**self.query_set).order_by(
            self.order_by) if self.order_by else Store.product_class.objects.filter(**self.query_set)

        return query_set[self.limits[0]:self.limits[1]] if self.limits else query_set


class Category:
    pass

    # class Product:
    #     @staticmethod
    #     def byProductId(product_id):
    #         return get_object_or_404(Store.product_class, pk=product_id)
    #
    #     @staticmethod
    #     def byCategoryId(category_id):
    #         return get_object_or_404(Store.product_class, category_id=category_id)
    #
    #     @staticmethod
    #     def byStoreId(store_id):
    #         return get_object_or_404(Store.product_class, store_id=store_id)
    #
    #     @staticmethod
    #     def getProductsOfStoreByStoreId(store_id):
    #         return Store.product_class.objects.get(store_id=store_id)
    #
    #     @staticmethod
    #     def getProductById(product_id):
    #         return Store.product_class.objects.get(id=product_id)
    #
    #     @staticmethod
    #     def getAllProducts():
    #         return Store.category_class.objects.all()
    #
    #     @staticmethod
    #     def getCategoryProductsByCategoryId(category_id):
    #         return Store.product_class.objects.filter(category_id=category_id)
    #
    #     @staticmethod
    #     def getCategoryProductsOfStore(category_id, store_id):
    #         return Store.product_class.objects.filter(category_id=category_id, store_id=store_id)
