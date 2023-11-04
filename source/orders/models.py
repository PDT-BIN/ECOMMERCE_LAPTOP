from django.db import models
from django.db.models import Q
from profiles.models import Customer, Employee
from controls.models import Laptop


class DeliveryAddress(models.Model):
    fullname = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=25)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class State(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    address = models.TextField()
    state = models.ForeignKey(State, on_delete=models.PROTECT, default=1)
    confirm_employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='confirm_orders')
    deliver_employee = models.ForeignKey(
        Employee, on_delete=models.PROTECT, null=True, blank=True, related_name='deliver_orders')
    laptops = models.ManyToManyField(
        Laptop, related_name='orders', through='OrderDetails', through_fields=('order', 'laptop'))

    class Meta:
        ordering = ['-created']

    @property
    def total(self) -> float:
        return sum([detail.price for detail in OrderDetails.objects.filter(order=self)])


class OrderDetails(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.PROTECT)

    class Meta:
        constraints = [models.CheckConstraint(check=Q(price__gt=0), name='CK_ORDER_PRICE')]


class ReturnForm(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    order = models.OneToOneField(Order, on_delete=models.PROTECT)
    return_details = models.ManyToManyField(
        OrderDetails, through='ReturnDetails', through_fields=('return_form', 'order_detail'))


class ReturnDetails(models.Model):
    return_form = models.ForeignKey(ReturnForm, on_delete=models.CASCADE)
    order_detail = models.ForeignKey(OrderDetails, on_delete=models.PROTECT)
