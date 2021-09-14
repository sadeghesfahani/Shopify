from .errors import handleError
from .market_manager import BaseMarketObjectManager
from .models import Category as CategoryModel
from copy import deepcopy


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
    # def getChildrenList(self, pk):
    #     parent = self.selectById(pk)
    #     children_list = list()
    #     parent_list = [parent]
    #     while self.targetObject.objects.filter(parent__in=parent_list).count() > 0:
    #         parent_list_copy = deepcopy(parent_list)
    #         parent_list = list()
    #         for child in self.targetObject.objects.filter(parent__in=parent_list_copy):
    #             children_list.append(child.id)
    #             parent_list.append(child.id)
    #     return children_list
    #
    # def addNew(self,category_data):
    #     new_category = self.targetObject(**CategoryDataStructure(**category_data).__dict__)
    #     new_category.save()
    #     return new_category


class CategoryDataStructure:
    def __init__(self, name, parent=None):
        self.name = name
        if isinstance(parent, int) or isinstance(parent, str):
            self.parent = Category().selectById(parent)
        elif parent is None:
            self.parent = None
        else:
            self.parent = parent
