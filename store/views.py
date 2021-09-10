from django.urls import reverse
from django.views.generic import TemplateView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins, generics, viewsets, permissions
from rest_framework.views import APIView

from .market import Market
from .store import *
from store.serializers import *


class HomeView(TemplateView):
    template_name = 'index.html'
    store = StoreObj()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['data'] = self.store.product.category(1).fetch()
        context['link'] = reverse("market-list")
        return context


class ProductApi(APIView):
    store = StoreObj()

    def get(self, request, *args, **kwargs):
        query_set = self.store.product.category(category_id=kwargs)
        serialized = ProductSerializer(query_set, many=True)
        return Response(serialized.data)


class CategoryApi(APIView):
    store = StoreObj()

    def get(self, request, *args, **kwargs):
        if 'category_id' in kwargs:
            query_set = self.store.product.category(kwargs['category_id']).fetch()
            serialized = ProductSerializer(query_set, many=True)
        else:
            query_set = self.store.category_class.objects.all()
            serialized = CategorySerializer(query_set, many=True)
        return Response(serialized.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = self.store.category.addCategory(CategoryDataStructure(**serializer.data))
            serializer = CategorySerializer(category)
            return Response(serializer.data)


class StoreApi(APIView):
    store = StoreObj()

    def get(self, request, *args, **kwargs):
        if 'store_id' in kwargs:
            query_set = self.store.product.store(kwargs['store_id']).fetch()
            serialized = ProductSerializer(query_set, many=True)
        else:
            query_set = self.store.store_class.objects.all()
            serialized = CategorySerializer(query_set, many=True)
        return Response(serialized.data)


class MenuApi(APIView):
    store = StoreObj()

    def get(self, request, *args, **kwargs):
        query_set = self.store.category_class.objects.all()
        serialized = MenuSerializer(query_set, many=True)
        return Response(serialized.data)


# ---------------------------------here----------------------------------------


class ProductAPI(viewsets.ViewSet):

    @staticmethod
    def list(request):
        queryset = Market(request).product.fetch()
        serialized = ProductSerializer(queryset, many=True)
        return Response(serialized.data)

    @staticmethod
    def retrieve(request, pk=None):
        market = Market(request)
        return Response(ProductSerializer(market.product.selectById(pk)).data)

    def create(self, request):
        market = Market(request)
        new_product = market.product.addNew(product_data=self.prepareData(market))
        serialized_new_product = ProductSerializer(new_product)
        return Response(serialized_new_product.data)

    def update(self, request, pk=None):
        market = Market(request)
        modified_product = market.product.modify(pk, self.prepareData(market))
        serialized_modified_product = ProductSerializer(modified_product)
        return Response(serialized_modified_product.data)

    def prepareData(self, market):
        store = market.admin.getStore()
        data = self.request.data
        data['store'] = store
        return data
