from .product import Product
from .category import Category
from .store import Store
from .data_structures import *
from .Users import *
from store.models import Store as StoreModel, Category as CategoryModel


class Market:
    """
    this class has been made to have full control over the business model and provide flexibility between separated
    models yet integrated business model, based on single responsibility principle and open-close principle, all classes
    build separately to have the least interaction with each other that may cause fragility during adding new features.
    """

    def __init__(self, request=None):
        self.product = Product(request)
        self.store = Store(request)
        self.customer = Customer(request)
        self.admin = Admin(request)
        self.category = Category(request)



















