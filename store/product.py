from rest_framework.exceptions import PermissionDenied

from shopify_first_try.utils import getObject
from .errors import handleError
from .market_manager import BaseMarketObjectManager
from .models import Product as ProductModel, Attribute as AttributeModel, Option as OptionModel, Price as PriceModel
from .store import Store
from .category import Category


class Product(BaseMarketObjectManager):
    targetObject = ProductModel

    def __init__(self, request=None):
        self.priceObject = Price()
        self.attribute = Attribute()
        super(Product, self).__init__(request)

    def filterByCategory(self, category_id, recursive=False):
        if recursive:
            children = Category().getAllChildren(category_id,True)
            if children is None or children == []:
                children = [category_id]
            self.querySet['category_id__in'] = children
        else:
            self.querySet["category_id"] = category_id
        return self

    def filterByStore(self, store_id):
        self.querySet['store_id'] = store_id
        return self

    @handleError(targetObject)
    def addNew(self, product_data):
        new_product = self.targetObject(**ProductDataStructure(**product_data).__dict__)
        new_product.save()
        self.priceObject.addNew(product=new_product, price=new_product.price)
        self.handleAttributes(new_product.id)

        return new_product

    @handleError(targetObject)
    def modify(self, product_id, product_data):
        product_to_modify = self.selectById(product_id)
        price = product_to_modify.price
        product_to_modify.__dict__.update(**ProductDataStructure(self.request, **product_data).__dict__)
        if product_to_modify.price != price:
            new_price_object = self.priceObject.addNew(product=product_to_modify, price=price)
            new_price_object.save()
        product_to_modify.save()
        self.handleAttributes(product_to_modify.id)
        product_to_modify = self.selectById(product_id)
        return product_to_modify

    @handleError(targetObject)
    def handleAttributes(self, product_id):
        (existing_attribute_ids, existing_option_ids) = (list(), list())

        if 'attributes' in self.request.data:

            for attr in self.request.data['attributes']:
                self.handleEachAttribute(attr, product_id, existing_attribute_ids, existing_option_ids)

            self.deleteResidualAttributesAndOptions(attribute_id_list=existing_attribute_ids,
                                                    option_id_list=existing_option_ids,
                                                    product_id=product_id)

    def handleEachAttribute(self, attr, product_id, existing_attribute_ids, existing_option_ids):
        if 'product' not in attr:
            attr['product'] = product_id
        if 'id' in attr:
            if self.isProductTheSame(product_id, attr['id']):
                Attribute().modifyAttribute(attribute_data_structure=AttributeDataStructure(**attr),
                                            attribute_id=attr['id'])
            else:
                raise PermissionDenied("product id your attribute is mentioning is belong to another products")
        else:
            new_made_attribute = Attribute().addNewAttribute(product_id=product_id,
                                                             attribute_data_structure=(
                                                                 AttributeDataStructure(**attr)))
            (attr['id'], attr['attribute']) = (new_made_attribute.id, new_made_attribute.id)

        existing_attribute_ids.append(attr['id'])
        self.handleOptions(attr, existing_option_ids)

    def handleOptions(self, attr, existing_option_ids):
        if 'options' in attr:
            for opt in attr["options"]:
                opt['attribute'] = attr['id']
                if 'id' in opt:
                    if self.isAttributeTheSame(attr['id'], opt['id']):
                        Option().modifyOption(option_id=opt['id'],
                                              option_data_structure=OptionDataStructure(**opt))
                    else:
                        raise PermissionDenied(
                            'your option is mentioning to an option does not belong to this attribute')
                else:
                    opt['attribute'] = attr["id"]
                    new_made_option = Option().addNewOption(attribute_id=attr["id"],
                                                            option_data_structure=OptionDataStructure(**opt))
                    opt['id'] = new_made_option.id
                existing_option_ids.append(opt['id'])

    @staticmethod
    def isProductTheSame(product_id, attribute_id):
        return True if Attribute().getAttributeById(attribute_id).product_id == product_id else False

    @staticmethod
    def isAttributeTheSame(attribute_id, option_id):
        return True if Option().selectById(option_id).attribute_id == attribute_id else False

    @staticmethod
    def deleteResidualAttributesAndOptions(attribute_id_list, option_id_list, product_id):
        attribute_object = Attribute()
        option_object = Option()
        product_attributes = attribute_object.getProductAttributes(product_id)
        for attribute in product_attributes:
            if attribute.id not in attribute_id_list:
                attribute_object.removeAttributeById(attribute.id)
            else:
                options = attribute_object.getAttributeOptions(attribute.id)
                [option_object.removeOptionById(option.id) for option in options if option.id not in option_id_list]


class Attribute:
    targetObject = AttributeModel

    def __init__(self):
        self.option = Option()

    def getProductAttributes(self, product_id):
        return self.targetObject.objects.filter(product_id=product_id)

    @handleError(targetObject)
    def getAttributeOptions(self, attribute_id):
        return self.targetObject.objects.get(pk=attribute_id).option_set.all()

    def addNewAttribute(self, product_id, attribute_data_structure):
        new_made_attribute = self.targetObject(product_id=product_id, **attribute_data_structure.__dict__)
        new_made_attribute.save()
        return new_made_attribute

    @handleError(targetObject)
    def modifyAttribute(self, attribute_data_structure, attribute_id):
        attribute_to_modify = self.targetObject.objects.get(pk=attribute_id)
        attribute_to_modify.__dict__.update(**attribute_data_structure.__dict__)
        attribute_to_modify.save()
        return attribute_to_modify

    @handleError(targetObject)
    def getAttributeById(self, attribute_id):
        return self.targetObject.objects.get(pk=attribute_id)

    @handleError(targetObject)
    def removeAttributeById(self, attribute_id):
        self.targetObject.objects.get(pk=attribute_id).delete()


class Option:
    targetObject = OptionModel

    def addNewOption(self, attribute_id, option_data_structure):
        new_made_option = self.targetObject(attribute_id=attribute_id, **option_data_structure.__dict__)
        new_made_option.save()
        return new_made_option

    @handleError(targetObject)
    def modifyOption(self, option_id, option_data_structure):
        option_to_modify = self.targetObject.objects.get(pk=option_id)
        option_to_modify.__dict__.update(**option_data_structure.__dict__)
        option_to_modify.save()
        return option_to_modify

    @handleError(targetObject)
    def removeOptionById(self, option_id):
        self.targetObject.objects.get(pk=option_id).delete()

    @handleError(targetObject)
    def selectById(self, option_id):
        return self.targetObject.objects.get(pk=option_id)


class Price:
    targetObject = PriceModel

    def addNew(self, product, price):
        new_price = self.targetObject(product=product, price=price)
        new_price.save()
        return new_price

    def getPriceList(self, product):
        return self.targetObject.objects.filter(product=product)


class AttributeDataStructure:
    def __init__(self, name, product, *args, **kwargs):
        self.name = name
        self.product = getObject(Product(), product)


class OptionDataStructure:
    def __init__(self, name, attribute, type, price, *args, **kwargs):
        self.name = name
        self.attribute = getObject(Attribute(), attribute)
        self.type = type
        self.price = price


class ProductDataStructure:
    """
    this data structure will always come into place to avoid and handle unexpected errors during transforming information
    """

    def __init__(self, name, category, description, store, price=None, *args, **kwargs):
        self.name = name
        self.category = getObject(Category(), category)
        self.description = description
        self.store = getObject(Store(), store)
        self.price = price
