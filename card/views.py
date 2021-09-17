from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, generics


class CardAPI(viewsets.ViewSet, generics.GenericAPIView):
    def create(self,request,*args,**kwargs):
        pass