from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.views import APIView

from store.serializers import CategorySerializer


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['hi'] = 'hi'
        return context


class CategoryApi(APIView):
    serializer_class = CategorySerializer
