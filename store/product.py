from .market_manager import BaseMarketObjectManager
from .models import Product as ProductModel, Attribute as AttributeModel, Option as OptionModel, Price as PriceModel
from .store import Store
from .category import Category


class Product(BaseMarketObjectManager):
    targetObject = ProductModel

    def __init__(self, request):
        self.priceObject = Price()
        self.attribute = Attribute()
        super(Product, self).__init__(request)

    def filterByCategory(self, category_id, recursive=False):
        if recursive:
            children = Category().getChildrenList(category_id)
            if children is None or children == []:
                children = [category_id]
            self.querySet['category_id__in'] = children
        else:
            self.querySet["category_id"] = category_id
        return self

    def filterByStore(self, store_id):
        self.querySet['store_id'] = store_id
        return self

    def addNew(self, product_data):
        new_product = self.targetObject(**ProductDataStructure(self.request, **product_data).__dict__)
        new_product.save()
        self.priceObject.addNew(product=new_product, price=new_product.price)
        return new_product

    def modify(self, product_id, product_data):
        product_to_modify = self.selectById(product_id)
        price = product_to_modify.price
        product_to_modify.__dict__.update(**ProductDataStructure(self.request, **product_data).__dict__)
        if product_to_modify.price != price:
            new_price_object = self.priceObject.addNew(product=product_to_modify, price=price)
            new_price_object.save()
        product_to_modify.save()
        return product_to_modify


class Attribute:
    targetObject = AttributeModel

    def __init__(self):
        self.option = Option()

    def getProductAttributes(self, product_id):
        return self.targetObject.objects.filter(product_id=product_id)

    def getAttributeOptions(self, attribute_id):
        return self.targetObject.objects.get(pk=attribute_id).option_set.all()

    def addNewAttribute(self, attribute_data_structure):
        return self.targetObject(**attribute_data_structure.__dict__).save()

    def modifyAttribute(self, attribute_data_structure, attribute_id):
        attribute_to_modify = self.targetObject.objects.get(pk=attribute_id)
        attribute_to_modify.__dict__.update(**attribute_data_structure.__dict__)
        attribute_to_modify.save()
        return attribute_to_modify


class Option:
    targetObject = OptionModel

    def addNewOption(self, attribute_id, option_data_structure):
        return self.targetObject(attribute_id=attribute_id, **option_data_structure.__dict__).save()

    def modifyOption(self, option_id, option_data_structure):
        option_to_modify = self.targetObject.objects.get(pk=option_id)
        option_to_modify.__dict__.update(**option_data_structure.__dict__)
        option_to_modify.save()
        return option_to_modify


# todo: create datastructures

class Price:
    targetObject = PriceModel

    def addNew(self, product, price):
        return self.targetObject(product=product, price=price).save()

    def getPriceList(self, product):
        return self.targetObject.objects.filter(product=product)


class ProductDataStructure:
    """
    this data structure will always come into place to avoid and handle unexpected errors during transforming information
    """

    def __init__(self, request, name, category, description, store, price=None):
        self.name = name
        if isinstance(category, int) or isinstance(category, str):
            self.category = Category().selectById(category)
        else:
            self.category = category
        self.description = description
        if isinstance(store, int) or isinstance(store, str):
            self.store = Store().selectById(store)
        else:
            self.store = store
        self.price = price
