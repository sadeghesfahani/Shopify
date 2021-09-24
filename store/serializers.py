from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'shown_in_menu_bar', 'level']


class CustomCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class AttributeSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Attribute
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    attributes = AttributeSerializer(many=True)
    image = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = '__all__'

    # def price(self):
    #     return PriceSerializer(self.price)


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        depth = 1


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 3
