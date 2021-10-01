from account.models import Address as AddressModel
from shopify_first_try.utils import getObject
from store.errors import handleError
from django.contrib.auth import get_user_model

User = get_user_model()


class Address:
    targetObject = AddressModel

    @handleError(targetObject)
    def selectByUser(self, user):
        user_model = getObject(User, user)
        return self.targetObject.objects.filter(user=user_model)

    def addAddress(self, data):
        structured_data = AddressDataStructure(data)
        newly_added_address = self.targetObject(**structured_data.__dict__)
        newly_added_address.save()
        return newly_added_address

    @handleError(targetObject)
    def editAddress(self, address_id, **kwargs):
        structured_data = AddressDataStructure(kwargs)
        address_to_edit = self.targetObject.objects.get(pk=address_id)
        address_to_edit.__dict__.update(**structured_data.__dict__)
        address_to_edit.save()
        return address_to_edit


class AddressDataStructure:
    def __init__(self, *args, **kwargs):
        self.address = kwargs.get('address')
        self.postal_code = kwargs.get('postal_code')
        self.user = getObject(User, kwargs.get('user'))
