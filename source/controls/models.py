from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from profiles.models import Customer, Employee


class Specification(models.Model):
    os = models.CharField(max_length=200)
    ram = models.CharField(max_length=200)
    cpu = models.CharField(max_length=200)
    disk = models.CharField(max_length=200)
    vga = models.CharField(max_length=200)
    battery = models.FloatField()
    screensize = models.FloatField()
    resolution = models.CharField(max_length=50)
    weight = models.FloatField()

    class Meta:
        unique_together = ('os', 'ram', 'cpu', 'disk', 'vga', 'battery', 'screensize', 'resolution', 'weight')

    def __str__(self) -> str:
        return f'{self.os} - {self.ram} - {self.cpu}'


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    specifications = models.ManyToManyField(
        Specification, related_name='manufacturers',
        through="LaptopModel", through_fields=('manufacturer', 'specification'))

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class LaptopModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.PROTECT)
    specification = models.ForeignKey(Specification, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', default='img/default.jpg')
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    cart_details = models.ManyToManyField(
        Customer, related_name='cart_details', through='CartDetails',
        through_fields=('laptop_model', 'customer'))

    class Meta:
        ordering = ['-id']
        constraints = [models.CheckConstraint(check=Q(price__gt=0), name='CK_MODEL_PRICE'),
                       models.CheckConstraint(check=Q(quantity__gte=0), name='CK_MODEL_QUANTITY')]

    def __str__(self) -> str:
        return f'{self.name} - {self.specification.pk}'

    def can_delete(self) -> bool:
        return not self.reservationdetails_set.all()


class CartDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    laptop_model = models.ForeignKey(LaptopModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.CheckConstraint(check=Q(quantity__gt=0), name='CK_CART_QUANTITY')]


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class ReservationForm(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    reservation_details = models.ManyToManyField(
        LaptopModel, blank=True, through='ReservationDetails',
        through_fields=('reservation_form', 'laptop_model'))

    class Meta:
        ordering = ['-created']

    @property
    def total(self) -> float:
        return sum([detail.quantity * detail.price for detail in
                    ReservationDetails.objects.filter(reservation_form=self)])

    @property
    def can_delete(self) -> bool:
        return not ImportationForm.objects.filter(reservation_form=self)


class ReservationDetails(models.Model):
    reservation_form = models.ForeignKey(ReservationForm, on_delete=models.CASCADE)
    laptop_model = models.ForeignKey(LaptopModel, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        constraints = [models.CheckConstraint(check=Q(quantity__gt=0), name='CK_RESERVATION_DETAILS_QUANTITY')]


class ImportationForm(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    reservation_form = models.OneToOneField(ReservationForm, on_delete=models.PROTECT)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    importation_details = models.ManyToManyField(
        ReservationDetails, through='ImportationDetails',
        through_fields=('importation_form', 'reservations_detail'))

    class Meta:
        ordering = ['-created']

    @property
    def total(self) -> float:
        return sum([detail.quantity * detail.reservations_detail.price for detail in
                    ImportationDetails.objects.filter(importation_form=self)])

    @property
    def can_delete(self) -> bool:
        return datetime.today().timestamp() < (self.created + timedelta(days=1)).timestamp()

    def can_update(self, details: list[str, int]) -> bool:
        for detail_id, quantity in details:
            detail = ReservationDetails.objects.get(pk=detail_id)
            model = detail.laptop_model
            if importation_detail := ImportationDetails.objects.filter(reservations_detail=detail).first():
                if model.quantity + quantity - importation_detail.quantity:
                    return False
        return True


class ImportationDetails(models.Model):
    importation_form = models.ForeignKey(ImportationForm, on_delete=models.CASCADE)
    reservations_detail = models.ForeignKey(ReservationDetails, on_delete=models.PROTECT)
    quantity = models.IntegerField()

    class Meta:
        constraints = [models.CheckConstraint(check=Q(quantity__gt=0), name='CK_IMPORTATION_DETAILS_QUANTITY')]

    def can_delete(self, quantity: int) -> bool:
        return self.reservations_detail.laptop_model.quantity - quantity > 0


class LiquidationForm(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)


class Laptop(models.Model):
    is_sold = models.BooleanField(default=False)
    laptop_model = models.ForeignKey(LaptopModel, on_delete=models.PROTECT)
    importation_form = models.ForeignKey(ImportationForm, on_delete=models.PROTECT)
    liquidation_form = models.OneToOneField(LiquidationForm, on_delete=models.PROTECT, null=True, blank=True)
