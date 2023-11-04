from math import ceil

from webapps import sessions
from django.http import HttpRequest
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
# DATA.
from django.db.models import Q
from django.db.transaction import atomic
from profiles.models import Employee, User
from profiles.forms import SignInForm
from orders.models import Order, OrderDetails, State
from . import models, forms
# PERMISSION.
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import AbstractBaseUser
# AI MODEL.
from .classification import make_predict


# HOME PAGE.
def home_page(request: HttpRequest):
    user = request.user
    if user.is_authenticated and (user.is_superuser or user.is_staff or user.is_shipper):
        logout(request)
        return redirect('signin')
    # CREATE CONTEXT.
    context = {}
    # GET DATA.
    categories = models.Category.objects.all()
    manufacturers = models.Manufacturer.objects.all()
    all_models = models.LaptopModel.objects.filter(quantity__gt=0)
    # GET CART & ADDRESS.
    if request.user.is_authenticated:
        cart_models = request.user.customer.cart_details.all()
        addresses = request.user.customer.deliveryaddress_set.all()
        context.update({'cart_models': cart_models, 'addresses': addresses})
    # FILTER.
    if kw := request.GET.get('kw', ''):
        all_models = all_models.filter(
            Q(name__icontains=kw) | Q(category__name__icontains=kw) |
            Q(manufacturer__name__icontains=kw) | Q(specification__os__icontains=kw) |
            Q(specification__ram__icontains=kw) | Q(specification__cpu__icontains=kw) |
            Q(specification__disk__icontains=kw) | Q(specification__vga__icontains=kw) |
            Q(specification__battery__icontains=kw) | Q(specification__weight__icontains=kw) |
            Q(specification__screensize__icontains=kw) | Q(specification__resolution__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(all_models) / 12)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    current_page = max(min(current_page, total_pages), 1)
    all_models = all_models[(current_page - 1) * 12:current_page * 12]
    # UPDATE CONTEXT.
    context.update({
        'categories': categories, 'manufacturers': manufacturers,
        'total_pages': total_pages, 'current_page': current_page,
        'show_models': all_models, 'keyword': kw, **sessions.get(request)
    })

    return render(request, 'home.html', context)


# DASHBOARD.
def dashboard_signin(request: HttpRequest):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('controls:employee')
        if user.is_staff:
            return redirect('controls:product')

    form = SignInForm(request)
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff or user.is_superuser:
                login(request, user)
                if user.is_superuser:
                    return redirect('controls:employee')
                if user.is_staff:
                    return redirect('controls:product')
            else:
                sessions.add(request, 'Đăng nhập thất bại', 'Tài khoản của bạn không có quyền truy cập', False)
        else:
            sessions.add(request, 'Đăng nhập thất bại', 'Thông tin không chính xác', False)

    context = {'form': form, **sessions.get(request)}
    return render(request, 'controls/signin.html', context)


def check_staff_permission(user: AbstractBaseUser) -> bool:
    return user.is_authenticated and (user.is_superuser or user.is_staff)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_password(request: HttpRequest):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            sessions.add(request, 'Thao tác thất bại', 'Mật khẩu xác nhận không trùng khớp', False)
        elif not user.check_password(password):
            sessions.add(request, 'Thao tác thất bại', 'Mật khẩu cũ không chính xác', False)
        else:
            user.set_password(password1)
            user.save()
            login(request, user)
            sessions.add(request, 'Thao tác thành công', 'Thay đổi mật khẩu thành công')

    context = {'section': 5, **sessions.get(request)}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_logout(request: HttpRequest):
    logout(request)
    return redirect('controls:signin')


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_employee(request: HttpRequest):
    results = Employee.objects.all()
    # FILTER.
    if kw := request.GET.get('kw', ''):
        results = results.filter(Q(pk__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(results) / 10)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    results = results[(current_page - 1) * 10:current_page * 10]

    context = {'section': 0, 'results': results, 'keyword': kw,
               'total_pages': total_pages, 'current_page': current_page}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_product(request: HttpRequest):
    results = models.LaptopModel.objects.all()
    # FILTER.
    if kw := request.GET.get('kw', ''):
        results = results.filter(
            Q(pk__icontains=kw) | Q(name__icontains=kw) | 
            Q(category__name__icontains=kw) | Q(manufacturer__name__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(results) / 10)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    results = results[(current_page - 1) * 10:current_page * 10]

    context = {'section': 1, 'results': results, 'keyword': kw,
               'total_pages': total_pages, 'current_page': current_page}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_reservation(request: HttpRequest):
    user = request.user
    results = models.ReservationForm.objects.all()
    if not user.is_superuser and user.is_staff:
        results = results.filter(employee=user.employee)
    # FILTER.
    if kw := request.GET.get('kw', ''):
        results = results.filter(Q(pk__icontains=kw) | Q(supplier__name__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(results) / 10)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    results = results[(current_page - 1) * 10:current_page * 10]

    context = {'section': 2, 'results': results, 'keyword': kw,
               'total_pages': total_pages, 'current_page': current_page}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_importation(request: HttpRequest):
    user = request.user
    results = models.ImportationForm.objects.all()
    if not user.is_superuser and user.is_staff:
        results = results.filter(employee=request.user.employee)
    # FILTER.
    if kw := request.GET.get('kw', ''):
        results = results.filter(Q(pk__icontains=kw) | Q(reservation_form__supplier__name__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(results) / 10)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    results = results[(current_page - 1) * 10:current_page * 10]

    context = {'section': 3, 'results': results, 'keyword': kw,
               'total_pages': total_pages, 'current_page': current_page}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def dashboard_order(request: HttpRequest):
    user = request.user
    results = Order.objects.all()
    if not user.is_superuser and user.is_staff:
        results = results.filter(Q(confirm_employee=None) | Q(confirm_employee=user.employee))
    # FILTER.
    if kw := request.GET.get('kw', ''):
        results = results.filter(Q(pk__icontains=kw))
    # PAGINATE.
    total_pages = ceil(len(results) / 10)
    control_page = int(request.GET.get('control', 0))
    current_page = int(request.GET.get('current_page', 1)) + control_page
    current_page = max(min(current_page, total_pages), 1)
    results = results[(current_page - 1) * 10:current_page * 10]

    context = {'section': 4, 'results': results, 'keyword': kw,
               'total_pages': total_pages, 'current_page': current_page}
    return render(request, 'controls/dashboard.html', context)


# EMPLOYEE.
@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def create_employee(request: HttpRequest):
    form = forms.EmployeeForm()

    if request.method == 'POST':
        form = forms.EmployeeForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')

        if not User.objects.filter(Q(username=username) | Q(email=email)).first():
            if form.is_valid():
                instance = form.save(commit=False)

                user = User.objects.create(username=username, email=email, is_active=True)
                user.set_password(password)
                if role == '0':
                    user.is_staff = True
                else:
                    user.is_shipper = True
                user.is_active = not instance.is_quit
                user.save()

                instance.user = user
                instance.save()

                return redirect('controls:employee')
        else:
            sessions.add(request, 'Thao tác thất bại', 'Tên tài khoản hoặc email đã tồn tài!', False)

    context = {'section': 0, 'form': form, 'action': True, 'task': 0, **sessions.get(request)}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def update_employee(request: HttpRequest, pk: int):
    result = get_object_or_404(Employee, pk=pk)
    form = forms.EmployeeForm(instance=result)

    if request.method == 'POST':
        form = forms.EmployeeForm(instance=result, data=request.POST)
        email = request.POST.get('email')

        if not User.objects.exclude(employee=result).filter(email=email):
            if form.is_valid():
                instance = form.save()
                user = instance.user

                user.email = email
                role = request.POST.get('role')
                if role == '0':
                    user.is_staff = True
                    user.is_shipper = False
                else:
                    user.is_staff = False
                    user.is_shipper = True
                user.is_active = not instance.is_quit

                user.save()
                print(user.is_active)
                return redirect('controls:employee')
        else:
            sessions.add(request, 'Thao tác thất bại', 'Email đã tồn tài!', False)

    context = {'section': 0, 'form': form, 'result': result, 'action': True, 'task': 1, **sessions.get(request)}
    return render(request, 'controls/dashboard.html', context)


# PRODUCT.
@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def create_specification(request: HttpRequest):
    form = forms.SpecificationForm()

    if request.method == 'POST':
        form = forms.SpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('controls:product')

    context = {'section': 1, 'form': form, 'action': True, 'task': 1}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def create_product(request: HttpRequest):
    specifications = models.Specification.objects.all()
    manufacturers = models.Manufacturer.objects.all()
    form = forms.ModelForm()

    if request.method == 'POST':
        form = forms.ModelForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            # MANUFACTURER.
            manufacturer, _ = models.Manufacturer.objects.get_or_create(name=request.POST.get('manufacturer'))
            instance.manufacturer = manufacturer
            # SPECIFICATION.
            specification = specifications.get(pk=request.POST.get('specification'))
            instance.specification = specification
            # CATEGORY.
            category = models.Category.objects.get(name=make_predict(instance))
            instance.category = category
            instance.save()
            return redirect('controls:product')

    context = {'section': 1, 'form': form, 'action': True, 'task': 0,
               'manufactures': manufacturers, 'specifications': specifications}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def update_product(request: HttpRequest, pk: int):
    manufacturers = models.Manufacturer.objects.all()
    result = get_object_or_404(models.LaptopModel, pk=pk)
    specifications = models.Specification.objects.exclude(pk=pk)
    form = forms.ModelForm(instance=result)

    if request.method == 'POST':
        form = forms.ModelForm(request.POST, request.FILES, instance=result)
        if form.is_valid():
            instance = form.save(commit=False)
            # MANUFACTURER.
            manufacturer, _ = models.Manufacturer.objects.get_or_create(name=request.POST.get('manufacturer'))
            instance.manufacturer = manufacturer
            # SPECIFICATION.
            specification = models.Specification.objects.get(pk=request.POST.get('specification'))
            instance.specification = specification
            # CATEGORY.
            category = models.Category.objects.get(name=make_predict(instance))
            instance.category = category
            instance.save()
            return redirect('controls:product')

    context = {'section': 1, 'form': form, 'action': True, 'task': 0,
               'manufactures': manufacturers, 'manufacturer': result.manufacturer,
               'specifications': specifications, 'main': result.specification}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def delete_product(request: HttpRequest, pk: int):
    result = get_object_or_404(models.LaptopModel, pk=pk)

    if request.method == 'POST':
        result.delete()
        return redirect('controls:product')

    context = {'section': 1, 'action': True, 'result': result}
    return render(request, 'controls/dashboard.html', context)


# RESERVATION.
@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def create_reservation(request: HttpRequest):
    suppliers = models.Supplier.objects.all()
    all_models = models.LaptopModel.objects.all()

    if request.method == 'POST':
        details = []
        for model_id in request.POST.getlist('model-list[]'):
            quantity = int(request.POST.get(model_id + '_Q'))
            price = float(request.POST.get(model_id + '_P'))
            details.append((model_id, quantity, price))

        supplier, _ = models.Supplier.objects.get_or_create(name=request.POST.get('supplier'))
        form = models.ReservationForm.objects.create(supplier=supplier, employee=request.user.employee)
        if details:
            for model_id, quantity, price in details:
                model, quantity, price = all_models.get(pk=model_id), quantity, price
                models.ReservationDetails.objects.create(
                    reservation_form=form, laptop_model=model, quantity=quantity, price=price)
        return redirect('controls:reservation')

    context = {'section': 2, 'action': True, 'suppliers': suppliers, 'models': all_models}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def view_reservation(request: HttpRequest, pk: int):
    form = get_object_or_404(models.ReservationForm, pk=pk)
    reservation_details = models.ReservationDetails.objects.filter(reservation_form=form)

    context = {'section': 2, 'action': True, 'task': 0, 
               'form': form, 'details': reservation_details}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def update_reservation(request: HttpRequest, pk: int):
    form = get_object_or_404(models.ReservationForm, pk=pk)
    reservation_details = models.ReservationDetails.objects.filter(reservation_form=form)
    suppliers = models.Supplier.objects.all()
    all_models = models.LaptopModel.objects.all()

    if request.method == 'POST':
        details = []
        detail_ids = []
        for model_id in request.POST.getlist('model-list[]'):
            quantity = int(request.POST.get(model_id + '_Q'))
            price = float(request.POST.get(model_id + '_P'))
            details.append((model_id, quantity, price))
            detail_ids.append(model_id)

        supplier, _ = models.Supplier.objects.get_or_create(name=request.POST.get('supplier'))
        form.supplier = supplier
        form.save()
        if details:
            for model_id, quantity, price in details:
                model, quantity, price = all_models.get(pk=model_id), quantity, price
                models.ReservationDetails.objects.update_or_create(
                    reservation_form=form, laptop_model=model, defaults={'quantity': quantity, 'price': price})

            for detail in reservation_details:
                if str(detail.laptop_model.pk) not in detail_ids:
                    detail.delete()
        return redirect('controls:reservation')

    context = {'section': 2, 'action': True, 'task': 1, 'suppliers': suppliers,
               'models': all_models, 'form': form, 'details': reservation_details}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def delete_reservation(request: HttpRequest, pk: int):
    result = get_object_or_404(models.ReservationForm, pk=pk)

    if request.method == 'POST':
        result.delete()
        return redirect('controls:reservation')

    context = {'section': 2, 'action': True, 'result': result}
    return render(request, 'controls/dashboard.html', context)


# IMPORTATION.
@user_passes_test(test_func=check_staff_permission, login_url='signin')
@atomic
def create_importation(request: HttpRequest):
    employee = request.user.employee
    reservations = models.ReservationForm.objects.filter(employee=employee, importationform=None)
    reservation_details = models.ReservationDetails.objects.filter(reservation_form__in=reservations)

    if request.method == 'POST':
        details = []
        for detail_id in request.POST.getlist('model-list[]'):
            quantity = int(request.POST.get(detail_id + '_Q'))
            details.append((detail_id, quantity))

        reservation = reservations.get(pk=int(request.POST.get('reservation')))
        form = models.ImportationForm.objects.create(reservation_form=reservation, employee=employee)
        if details:
            for detail_id, quantity in details:
                detail, quantity = models.ReservationDetails.objects.get(pk=detail_id), quantity
                models.ImportationDetails.objects.create(
                    importation_form=form, reservations_detail=detail, quantity=quantity)

                model = detail.laptop_model
                model.quantity += quantity
                model.save()

                for _ in range(quantity):
                    models.Laptop.objects.create(laptop_model=model, importation_form=form)

        return redirect('controls:importation')

    context = {'section': 3, 'action': True, 'reservations': reservations,
               'reservation_details': reservation_details, 'task': 0}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def view_importation(request: HttpRequest, pk: int):
    form = get_object_or_404(models.ImportationForm, pk=pk)
    reservation_details = models.ReservationDetails.objects.filter(reservation_form=form.reservation_form)
    importation_details = models.ImportationDetails.objects.filter(importation_form=form)

    context = {'section': 3, 'action': True, 'reservation': form.reservation_form, **sessions.get(request),
               'reservation_details': reservation_details, 'importation_details': importation_details, 'task': 1}
    return render(request, 'controls/dashboard.html', context)


# ORDER.
@user_passes_test(test_func=check_staff_permission, login_url='signin')
def view_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    details = []
    for order_detail in OrderDetails.objects.filter(order=order):
        detail = [order_detail.laptop.laptop_model, 1, order_detail.price]
        existed_detail = list(filter(lambda e: e[0] == detail[0], details))
        if not existed_detail:
            details.append(detail)
        else:
            details[details.index(existed_detail[0])][1] += 1

    context = {'section': 4, 'action': True, 'task': 0, 'order': order, 'details': details}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def confirm_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    details = []
    for order_detail in OrderDetails.objects.filter(order=order):
        detail = [order_detail.laptop.laptop_model, 1, order_detail.price]
        existed_detail = list(filter(lambda e: e[0] == detail[0], details))
        if not existed_detail:
            details.append(detail)
        else:
            details[details.index(existed_detail[0])][1] += 1

    if request.method == 'POST':
        state = 2 if order.state.pk == 1 else 4
        order.state = State.objects.get(pk=state)
        order.confirm_employee = request.user.employee
        order.save()
        return redirect('controls:order')

    context = {'section': 4, 'action': True, 'task': 1, 'order': order, 'details': details}
    return render(request, 'controls/dashboard.html', context)


@user_passes_test(test_func=check_staff_permission, login_url='signin')
def deliver_order(request: HttpRequest, pk: int):
    order = get_object_or_404(Order, pk=pk)
    shippers = Employee.objects.filter(user__is_shipper=True)

    if request.method == 'POST':
        order.state = State.objects.get(pk=3)
        shipper = Employee.objects.get(pk=request.POST.get('shipper'))
        order.deliver_employee = shipper
        order.save()
        return redirect('controls:order')

    context = {'section': 4, 'action': True, 'task': 2, 'order': order, 'shippers': shippers}
    return render(request, 'controls/dashboard.html', context)
