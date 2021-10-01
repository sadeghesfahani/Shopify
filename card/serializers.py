from rest_framework import serializers
from .models import *


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['orders', 'additional_option', 'delivery', 'status', 'address_to_send_good',
                  'address_to_send_invoice', 'receive_time', 'total_cost', 'total_products_cost','discount']

