from django import forms

from profiles.models import Employee
from .models import LaptopModel, Specification


class SpecificationForm(forms.ModelForm):
    os = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    ram = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    cpu = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    disk = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    vga = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    battery = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'dashboard-input'
    }))

    screensize = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'dashboard-input', 'list': 'screensize-list'
    }))

    resolution = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }))

    weight = forms.FloatField(widget=forms.NumberInput(attrs={
        'class': 'dashboard-input'
    }))

    class Meta:
        model = Specification
        fields = '__all__'


class ModelForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'dashboard-input'
    }), required=True)

    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'dashboard-input', 'readonly': True, 'value': 0
    }), required=False)

    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'dashboard-input', 'min': 0
    }), required=True)

    class Meta:
        model = LaptopModel
        fields = '__all__'
        exclude = ['cart_details', 'category', 'manufacturer', 'specification']


class EmployeeForm(forms.ModelForm):
    last_name = forms.CharField(label='Họ', widget=forms.TextInput(attrs={
        'class': 'dashboard-input w-full'
    }), required=True)

    first_name = forms.CharField(label='Tên', widget=forms.TextInput(attrs={
        'class': 'dashboard-input w-full'
    }), required=True)

    gender = forms.BooleanField(label='Giới tính', widget=forms.RadioSelect(attrs={
        'class': 'flex ml-4 gap-10'
    }, choices=((True, 'Nam'), (False, 'Nữ'))), required=False)

    birthdate = forms.DateField(label='Ngày sinh', widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'dashboard-input w-full'
    }), required=True)

    address = forms.CharField(label='Địa chỉ', widget=forms.Textarea(attrs={
        'class': 'dashboard-input w-full'
    }), required=True)

    phone_number = forms.CharField(label='Số điện thoại', widget=forms.TextInput(attrs={
        'class': 'dashboard-input w-full'
    }), required=True)

    salary = forms.FloatField(label='Lương', widget=forms.NumberInput(attrs={
        'class': 'dashboard-input w-full'
    }), required=True)

    is_quit = forms.BooleanField(
        label='Đã nghỉ', widget=forms.CheckboxInput(), required=False)

    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']
