from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from .store import *
from store.serializers import *


class HomeView(TemplateView):
    template_name = 'index.html'
    store = StoreObj()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['data'] = self.store.product.category(1).fetch()
        return context


class ProductApi(APIView):
    store = StoreObj()

    def get(self, request,*args, **kwargs):
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
