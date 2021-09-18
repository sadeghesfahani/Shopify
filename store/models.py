from django.db import models
from django.contrib.auth import get_user_model
from django.utils.datetime_safe import date
from mptt.models import MPTTModel, TreeForeignKey

from account.models import Address

User = get_user_model()


class Category(MPTTModel):
    name = models.CharField(max_length=160, blank=False, null=False)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    shown_in_menu_bar = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        if self.get_ancestors().count() > 0:
            return f"{' - '.join([parent.name for parent in self.get_ancestors()])}-{self.name}"
        else:
            return f"{self.name}"


class Discount(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    code = models.CharField(max_length=60, null=True, blank=True)
    discount = models.IntegerField()
    users = models.ManyToManyField(User, blank=True)
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
    admins = models.ManyToManyField(User, related_name='admins', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, blank=False)
    description = models.CharField(max_length=1200, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, default=1)
    price = models.IntegerField()
    price_without_discount = models.IntegerField(default=0)
    quantity = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def attributes(self):
        attributes = Attribute.objects.filter(product_id=self.id)
        return attributes


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_product')
    price = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    price_without_discount = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            product = Product.objects.get(pk=self.product.id)
            product.price = self.price
            product.price_without_discount = self.price_without_discount
            product.save()
        return super(Price, self).save(*args, **kwargs)


class Attribute(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def options(self):
        return Option.objects.filter(attribute_id=self.id)


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

# class Card(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     WAITING_FOR_PAYMENT = 0
#     PENDING = 1
#     IN_PROCESS = 2
#     SENT = 3
#     DONE = 4
#     CHOICES = [
#         (WAITING_FOR_PAYMENT, 'Waiting to pay'),
#         (PENDING, 'Pending'),
#         (IN_PROCESS, 'In process'),
#         (SENT, 'Sent'),
#         (DONE, 'Done'),
#     ]
#     status = models.IntegerField(choices=CHOICES, default=0)
#     payment_info = models.CharField(max_length=160)
#     total_price = models.IntegerField()
#     discount = models.ForeignKey(Discount, on_delete=models.PROTECT)
#     address_to_send_good = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='cards_good')
#     address_to_send_invoice = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='cards_invoice')
#     receive_time = models.DateTimeField()
#
#
# class Order(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     options = models.ManyToManyField(Option)
#     attriubute_set = models.ForeignKey(AttributeSet, on_delete=models.CASCADE)
