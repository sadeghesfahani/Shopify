from django.db import models
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)


class Discount(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    discount = models.IntegerField()
    users = models.ManyToManyField(User, blank=True, null=True)
    limits = models.PositiveSmallIntegerField(blank=True, null=True)
    expire = models.DateTimeField(null=True, blank=True)

    USERS = 1
    FIRST_COME_FIRST_SERVE = 2
    DISCOUNT_CONDITION = [
        (USERS, 'target users'),
        (FIRST_COME_FIRST_SERVE, 'first come first serve'),
    ]
    discount_type = models.PositiveSmallIntegerField(choices=DISCOUNT_CONDITION)

    def is_valid(self, user):
        if self.discount_type == self.FIRST_COME_FIRST_SERVE:
            return True if self.isAnyThingLeft() and self.isTimeLeft() else False
        elif self.discount_type == self.USERS:
            return True if self.isUserAllowed(user) else False

    def isAnyThingLeft(self):
        return True if self.limits > 0 else False

    def isUserAllowed(self, user):
        return True if user in self.users else False

    def isTimeLeft(self):
        return True if date.today() < self.expire else False


class Store(models.Model):
    name = models.CharField(max_length=120)
    media = models.ImageField()


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=False,blank=False)
    description = models.CharField(max_length=1200,blank=True,null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)


class Media(models.Model):
    picture = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    MAIN = 1
    OTHER = 2
    INLINE = 3
    IMAGE_TYPE = [
        (MAIN, 'main picture'),
        (OTHER, 'other store pictures'),
        (INLINE, 'in content pictures'),
    ]
    picture_type = models.PositiveSmallIntegerField(choices=IMAGE_TYPE)


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()
