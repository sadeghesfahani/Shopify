from rest_framework import serializers

from store.models import Store


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=600)


class UserSerializerRegister(serializers.Serializer):
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)
    user_type = serializers.IntegerField()
    email = serializers.EmailField(max_length=120, required=True)
    password = serializers.CharField(max_length=120, required=True)


class UserSerializerShow(serializers.Serializer):
    counter = 0
    admins = serializers.SerializerMethodField()
    first_name = serializers.CharField(max_length=120, required=False)
    last_name = serializers.CharField(max_length=120, required=False)
    email = serializers.EmailField(max_length=120, required=True)
    user_type = serializers.IntegerField()

    def get_admins(self, instance):
        if self.counter == 0:
            self.counter += 1
            return Store.objects.filter(admins=instance)
