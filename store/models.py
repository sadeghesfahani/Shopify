from django.db import models
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date

from account.models import Address

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


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
    description = models.CharField(max_length=600)
    admins = models.ManyToManyField(User)


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=1200, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    @property
    def price(self):
        if len(self.price_set.all().order_by('-date')) > 0:
            return self.price_set.all().order_by('-date')[0]
        else:
            return 0


class Media(models.Model):
    picture = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, blank=True, null=True)
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
    date = models.DateTimeField(auto_now_add=True)


class Attribute(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)


class Option(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, blank=False, null=False)
    NONE = 0
    ABSOLUTE = 1
    RELATIVE = 2
    PERCENTIVE = 3
    CHOICES = [
        (NONE, 'no effect'),
        (ABSOLUTE, 'absolute'),
        (RELATIVE, 'relative'),
        (PERCENTIVE, 'percentive'),
    ]
    type = models.IntegerField(choices=CHOICES, default=0)
    price = models.IntegerField(default=0)


class AttributeSet(models.Model):
    options = models.ManyToManyField(Option)
    price = models.IntegerField(null=False, blank=False)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.IntegerField()


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    WAITING_FOR_PAYMENT = 0
    PENDING = 1
    IN_PROCESS = 2
    SENT = 3
    DONE = 4
    CHOICES = [
        (WAITING_FOR_PAYMENT, 'Waiting to pay'),
        (PENDING, 'Pending'),
        (IN_PROCESS, 'In process'),
        (SENT, 'Sent'),
        (DONE, 'Done'),
    ]
    status = models.IntegerField(choices=CHOICES, default=0)
    payment_info = models.CharField(max_length=160)
    total_price = models.IntegerField()
    discount = models.ForeignKey(Discount,on_delete=models.PROTECT)
    address_to_send_good = models.ForeignKey(Address)
    address_to_send_invoice = models.ForeignKey(Address)
    receive_time = models.DateTimeField()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    options = models.ManyToManyField(Option)
    attriubute_set = models.ForeignKey(AttributeSet)
