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


class HomeApi(APIView):
    store = StoreObj()

    def get(self, request):
        query_set = self.store.product.category(1).fetch()
        serialized = ProductSerializer(query_set,many=True)
        return Response(serialized.data)




class CategoryApi(APIView):
    store = StoreObj()

    def get(self, request,*args,**kwargs):
        query_set = self.store.product.category(kwargs['category_id']).fetch()
        serialized = ProductSerializer(query_set,many=True)
        return Response(serialized.data)