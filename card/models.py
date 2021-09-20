from django.contrib.auth import get_user_model
from django.db import models
from account.models import Address
from store.models import Product, Discount, Option

User = get_user_model()


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.SmallIntegerField()
    option = models.ForeignKey(Option, on_delete=models.PROTECT, null=True, blank=True)

    @property
    def order_price(self):
        if self.option is not None:
            if self.option.type == 0:
                return self.product.price * self.count
            elif self.option.type == 1:
                return self.option.price * self.count
            elif self.option.type == 2:
                return (self.product.price + self.option.price) * self.count
            else:
                return self.product.price * (1 + (self.option.price / 100)) * self.count
        else:
            return self.product.price * self.count

    def __str__(self):
        if self.option is not None:
            return f"{self.product.name} - {self.count} - {self.option.name}"
        else:
            return f"{self.product.name} - {self.count}"


class Delivery(models.Model):
    name = models.CharField(max_length=160)
    price = models.IntegerField()


class AdditionalOption(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    PERCENTIVE = 0
    ABSOLUTE = 1
    TYPES = [
        (PERCENTIVE, 'percentive'),
        (ABSOLUTE, 'absolute'),
    ]
    option_type = models.SmallIntegerField(choices=TYPES)
    cost = models.SmallIntegerField()


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    orders = models.ManyToManyField(Order, blank=True)
    discount = models.ForeignKey(Discount, on_delete=models.PROTECT,blank=True,null=True)
    additional_option = models.ForeignKey(AdditionalOption, models.PROTECT, blank=True, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.PROTECT)
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
    payment_info = models.CharField(max_length=160, blank=True, null=True)
    address_to_send_good = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='address_good')
    address_to_send_invoice = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='address_invoice',
                                                blank=True, null=True)
    receive_time = models.DateTimeField()

    @property
    def total_products_cost(self):
        total_cost = 0
        for order in self.orders.all():
            total_cost += order.order_price
        return total_cost * ((100 - self.discount.discount) / 100)

    @property
    def total_cost(self):
        if self.additional_option:
            if self.additional_option.option_type == 0:
                option_included_price = self.total_products_cost * (1 + self.additional_option.cost / 100)
            else:
                option_included_price = self.total_products_cost + self.additional_option.cost
        else:
            option_included_price = self.total_products_cost
        return self.delivery.price + option_included_price

    def save(self, *args, **kwargs):
        if self.status == 1:
            if self.discount.discount_type == self.discount.FIRST_COME_FIRST_SERVE:
                self.discount.limits -= 1
            elif self.discount.discount_type == self.discount.USERS:
                self.discount.users.remove(self.user)

            for order in self.orders.all():
                order.product.quantity -= order.count
                order.product.save()
            self.status = 2
            self.save()

        super(Card, self).save(*args, **kwargs)
