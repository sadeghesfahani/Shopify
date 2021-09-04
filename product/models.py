from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=60, blank=False, null=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)


class Discount(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    users = models.ManyToManyField(User, blank=True, null=True)
    limits = models.PositiveSmallIntegerField(blank=True, null=True)
    expire = models.DateTimeField(null=True, blank=True)
    USERS = 1
    CONDITIONAL = 2
    FIRST_COME_FIRST_SERVE = 3
    DISCOUNT_TYPE = [
        (USERS, 'target users'),
        (CONDITIONAL, 'expire date'),
        (FIRST_COME_FIRST_SERVE, 'first come first serve'),
    ]
    discount_type = models.PositiveSmallIntegerField(choices=DISCOUNT_TYPE)

    def is_valid(self, user):
        if self.discount_type == self.FIRST_COME_FIRST_SERVE:
            return True if self.isAnyThingLeft() else False
        elif self.discount_type == self.USERS:
            return True if self.isUserAllowed(user) else False
        elif self.discount_type == self.CONDITIONAL:
            return True  # todo : take care of conditional discount

    def isAnyThingLeft(self):
        return True if self.limits > 0 else False

    def isUserAllowed(self, user):
        return True if user in self.users else False


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1200)


class Media(models.Model):
    picture = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    MAIN = 1
    OTHER = 2
    INLINE = 3
    IMAGE_TYPE = [
        (MAIN, 'main picture'),
        (OTHER, 'other product pictures'),
        (INLINE, 'in content pictures'),
    ]
    picture_type = models.PositiveSmallIntegerField(choices=IMAGE_TYPE)


class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField()

