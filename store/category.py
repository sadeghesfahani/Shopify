from .market_manager import BaseMarketObjectManager
from .models import Category as CategoryModel
from copy import deepcopy


class Category(BaseMarketObjectManager):
    targetObject = CategoryModel

    def getChildrenList(self, pk):
        parent = self.selectById(pk)
        children_list = list()
        parent_list = [parent]
        while self.targetObject.objects.filter(parent__in=parent_list).count() > 0:
            parent_list_copy = deepcopy(parent_list)
            parent_list = list()
            for child in self.targetObject.objects.filter(parent__in=parent_list_copy):
                children_list.append(child.id)
                parent_list.append(child.id)
        return children_list
