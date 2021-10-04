from rest_framework import viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from card.card import Card, CardDataStructure, Delivery
from card.serializers import CardSerializer, DeliverySerializer, OptionSerializer
from store.discount import Discount
from .models import Delivery as DeliveryModel, AdditionalOption as OptionModel
from store.errors import handleError


class CardAPI(viewsets.ViewSet, generics.GenericAPIView):
    serializer_class = CardSerializer

    def __init__(self, *args, **kwargs):
        self.discount = Discount()
        self.card = Card()
        super(CardAPI, self).__init__(*args, **kwargs)

    def retrieve(self, request, pk=None):
        pass

    def list(self, request):
        card_object = Card()
        return Response(self.get_serializer_class()(card_object.selectByUser(request.user), many=True).data)

    def create(self, request):
        newly_added_card = self.card.addNew(user=request.user, **request.data)
        self.card.addOrderToCard(newly_added_card, request.data["orders"])
        if 'payment_info' in request.data and request.data['payment_info'] == 1:
            newly_added_card.status = 1
            newly_added_card.save()
        return Response(self.get_serializer_class()(newly_added_card, many=False).data)

    @action(detail=False)
    def discount_validation(self, request):
        code = request.GET.get('code')
        if self.discount.validate(self.request.user, code=code):
            discount_object = self.discount.getByCode(code)
            return Response({'status': True, "percent": discount_object.discount})
        return Response({'status': False})

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticated]
        return super(CardAPI, self).get_permissions()


class DeliveryAPI(viewsets.ViewSet, ListAPIView):
    serializer_class = DeliverySerializer
    queryset = DeliveryModel.objects.all()


class OptionsAPI(viewsets.ViewSet, ListAPIView):
    serializer_class = OptionSerializer
    queryset = OptionModel.objects.all()