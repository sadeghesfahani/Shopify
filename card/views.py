from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from store.discount import Discount
from store.errors import handleError


class CardAPI(viewsets.ViewSet, generics.GenericAPIView):
    def __init__(self, *args, **kwargs):
        self.discount = Discount()
        super(CardAPI, self).__init__(*args, **kwargs)

    def retrieve(self, request, pk=None):
        pass

    def list(self,request):
        return Response({'status':200})

    @action(detail=False)
    def discount_validation(self, request):
        code = request.GET.get('code')
        if self.discount.validate(self.request.user, code=code):
            return Response({'status': True})
        else:
            return Response({"status": False})

