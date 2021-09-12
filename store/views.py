from django.http import Http404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics, viewsets, permissions

from .market import Market
from store.serializers import *


class ProductAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = ProductSerializer
    queryset = None

    def list(self, request):
        try:
            return Response(self.prepareList())
        except Product.DoesNotExist:
            raise Http404

    def retrieve(self, request, pk=None):
        try:
            return Response(self.get_object(pk))
        except Product.DoesNotExist:
            raise Http404

    def create(self, request):

        try:
            return Response(self.createNewProduct())
        except Product.DoesNotExist:
            raise Http404

    def update(self, request, pk=None):
        try:
            return Response(self.modifyProduct(pk))
        except Product.DoesNotExist:
            raise Http404

    @action(detail=False)
    def find(self, request, pk=None):
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
        store = market.admin.getStore()
        data = self.request.data
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
            self.permission_classes = [permissions.IsAuthenticated]
        return super(ProductAPI, self).get_permissions()
