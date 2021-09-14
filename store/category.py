from .errors import handleError
from .market_manager import BaseMarketObjectManager
from .models import Category as CategoryModel


class Category(BaseMarketObjectManager):
    targetObject = CategoryModel

    @handleError(targetObject)
    def getChildren(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_children()

    @handleError(targetObject)
    def getAllChildren(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_descendants(include_self=False)

    @handleError(targetObject)
    def getFamily(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_family()

    @handleError(targetObject)
    def getParents(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_ancestors(include_self=False)

    @handleError(targetObject)
    def getParent(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_ancestors(ascending=True, include_self=False)[0]

    @handleError(targetObject)
    def getRoot(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_root()

    @handleError(targetObject)
    def getSiblings(self, category_id):
        return self.targetObject.objects.get(pk=category_id).get_siblings(include_self=True)

    @handleError(targetObject)
    def getRoots(self):
        return self.targetObject.objects.root_nodes()

    @handleError(targetObject)
    def addNew(self, category_data):
        new_category = self.targetObject(**CategoryDataStructure(**category_data).__dict__)
        new_category.save()
        return new_category

    @handleError(targetObject)
    def modifyCategory(self, category_id, category_data):
        category_to_modify = self.selectById(category_id)
        category_to_modify.__dict__.update(**CategoryDataStructure(**category_data).__dict__)
        category_to_modify.save()
        return category_to_modify


class CategoryDataStructure:
    def __init__(self, name, parent=None, shown_in_menu_bar=True, *args, **kwargs):
        self.name = name
        if isinstance(parent, int) or isinstance(parent, str):
            self.parent = Category().selectById(parent)
        elif parent is None:
            self.parent = None
        else:
            self.parent = parent
        self.shown_in_menu_bar = shown_in_menu_bar
