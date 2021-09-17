import mptt
from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions

from shopify_first_try import settings
from .errors import handleError
from .market import Market
from store.serializers import *
from .permissions import CategoryPermission, ProductPermissionCreate, ProductPermissionEdit


class CategoryAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = CategorySerializer
    queryset = Category

    def list(self, request):
        return Response(self.prepareList())

    def create(self, request):
        return Response(self.createNewCategory())

    def retrieve(self, request, pk=None):
        return Response(self.get_object(pk))

    def update(self, request, pk=None):
        return Response(self.modifyCategory(pk))

    @action(detail=True)
    def children(self, request, pk=None):
        market = Market(request)
        return Response(self.serializer_class(market.category.getChildren(pk), many=True).data)

    @action(detail=True)
    def all_children(self, request, pk=None):
        market = Market(request)
        return Response(self.serializer_class(market.category.getAllChildren(pk), many=True).data)

    @action(detail=True)
    def family(self, request, pk=None):
        market = Market(request)
        return Response(self.serializer_class(market.category.getFamily(pk), many=True).data)

    @action(detail=True)
    def all_parents(self, request, pk=None):
        market = Market(request)
        if 'self' in request.GET:
            return Response(self.serializer_class(market.category.getParents(pk, True), many=True).data)
        else:
            return Response(self.serializer_class(market.category.getParents(pk), many=True).data)

    @action(detail=True)
    def parent(self, request, pk=None):
        market = Market(request)
        parents = market.category.getParent(pk)
        include_self = False
        if 'self' in request.GET:
            include_self = True
        try:
            len(parents)
            return Response(self.serializer_class(market.category.getParent(pk, include_self), many=True).data)
        except TypeError:
            return Response(self.serializer_class(market.category.getParent(pk, include_self), many=False).data)

    @action(detail=True)
    def get_root(self, request, pk=None):
        market = Market(request)
        return Response(self.serializer_class(market.category.getRoot(pk), many=False).data)

    @action(detail=False)
    def roots(self, request):
        market = Market(request)
        try:
            return Response(self.serializer_class(market.category.getRoots(), many=True).data)
        except TypeError:
            return Response(self.serializer_class(market.category.getRoots(), many=False).data)

    def createNewCategory(self):
        market = Market(self.request)
        new_made_category = market.category.addNew(self.request.data)
        return self.serializer_class(new_made_category, many=False).data

    def prepareList(self):
        market = Market(self.request)
        serialized_data = self.serializer_class(market.category.fetch(), many=True)
        return serialized_data.data

    def get_object(self, pk=None):
        market = Market(self.request)
        category_selected = market.category.selectById(pk)
        return self.serializer_class(category_selected, many=False).data

    def modifyCategory(self, pk=None):
        market = Market(self.request)
        modified_category = market.category.modifyCategory(category_id=pk, category_data=self.request.data)
        return self.serializer_class(modified_category, many=False).data

    def get_permissions(self):
        if self.action == "create" or self.action == "update":
            self.permission_classes = [CategoryPermission]
        return super(CategoryAPI, self).get_permissions()


class ProductAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = None

    def list(self, request):
        return Response(self.prepareList())

    def retrieve(self, request, pk=None):
        return Response(self.get_object(pk))

    def create(self, request):
        return Response(self.createNewProduct())

    def update(self, request, pk=None):
        return Response(self.modifyProduct(pk))

    @action(detail=False)
    def find(self, request):
        products = self.get_queryset()
        if 'store' in request.GET:
            products.filterByStore(request.GET['store'])
        if 'category' in request.GET:
            if 'recursive' in request.GET and request.GET['recursive']:

                products.filterByCategory(request.GET['category'], True)
            else:
                products.filterByCategory(request.GET['category'])
        if 'orderby' in request.GET:
            products.orderBy(request.GET['orderby'])
        if 'low' in request.GET and 'high' in request.GET:
            products.limitsBy(int(request.GET['low']), int(request.GET['high']))

        return Response(self.get_serializer_class()(products.fetch(), many=True).data)

    def prepareData(self):
        market = Market(self.request)
        data = self.request.data
        if 'store' not in self.request.data:
            try:
                store = market.admin.getStore()
            except Store.DoesNotExist:
                store = settings.MEGA_STORE_ID
            data['store'] = store
        return data

    def get_object(self, pk=None):
        serializer = self.get_serializer_class()
        return serializer(self.get_queryset().selectById(pk)).data

    def get_queryset(self, many=False, pk=None):
        market = Market(self.request)
        if many:
            return market.product.fetch()
        return market.product

    def prepareList(self):
        serializer = self.get_serializer_class()
        queryset = self.get_queryset(many=True)
        return serializer(queryset, many=True).data

    def createNewProduct(self):
        new_product = self.get_queryset().addNew(product_data=self.prepareData())
        serialized_new_product = self.get_serializer_class()(new_product)
        return serialized_new_product.data

    def modifyProduct(self, pk):
        modified_product = self.get_queryset().modify(pk, self.prepareData())
        serialized_modified_product = self.get_serializer_class()(modified_product)
        return serialized_modified_product.data

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [ProductPermissionCreate]
        elif self.action == 'update':
            self.permission_classes = [ProductPermissionEdit]
        return super(ProductAPI, self).get_permissions()
