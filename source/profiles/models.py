from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_shipper = models.BooleanField(default=False)
    first_name = None
    last_name = None

    @property
    def role(self) -> str:
        return 'Vận chuyển' if self.is_shipper else 'Bán hàng'


class Person(models.Model):
    last_name = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    gender = models.BooleanField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.PROTECT)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'

    @property
    def fullname(self) -> str:
        return f'{self.last_name} {self.first_name}'


class Employee(Person):
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_quit = models.BooleanField(default=False)


class Customer(Person):
    pass
