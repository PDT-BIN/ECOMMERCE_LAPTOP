from webapps import sessions
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
# DATA.
from django.db.transaction import atomic
from controls.models import LaptopModel, CartDetails, Laptop
from . import models
# PERMISSION.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import user_passes_test


def check_customer_permission(user: AbstractBaseUser) -> bool:
    return user.is_authenticated and not (user.is_superuser or user.is_staff or user.is_shipper)


# ORDER.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def order_page(request: HttpRequest, choice: int):
    customer = request.user.customer
    orders = models.Order.objects.filter(customer=customer)
    cart_models = customer.cart_details.all()
    states = models.State.objects.all()
    # FILTER BY STATE.
    if choice != 0:
        orders = orders.filter(state__pk=choice)
    # FILTER BY ORDER ID.
    if kw := request.GET.get('kw'):
        orders = orders.filter(pk=int(kw))
    # ORDER RESULT.
    result = []
    for order in orders:
        order_details = models.OrderDetails.objects.filter(order=order)
        # ORDER TOTAL.
        total = sum(map(lambda detail: detail.price, order_details))
        # ORDER DETAILS.
        details = []
        for order_detail in order_details:
            detail = [order_detail.laptop.laptop_model, 1, order_detail.price]
            existed_detail = list(filter(lambda e: e[0] == detail[0], details))
            if not existed_detail:
                details.append(detail)
            else:
                details[details.index(existed_detail[0])][1] += 1
        result.append((order, details, total))

    context = {'orders': result, 'states': states, 'choice': choice,
               'cart_models': cart_models, **sessions.get(request)}
    return render(request, 'orders/list.html', context)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
@atomic
def create_order(request: HttpRequest):
    # GET DATA.
    customer = request.user.customer
    details = CartDetails.objects.filter(customer=customer)
    if details:
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        delivery_address = f'{fullname}, {phone}, {address}'
        # CREATE ORDER.
        order = models.Order.objects.create(customer=customer, address=delivery_address)
        # CREATE ORDER DETAILS.
        for detail in details:
            if detail.laptop_model.quantity > 0:
                model = detail.laptop_model
                for laptop in Laptop.objects.filter(laptop_model=model, is_sold=False)[:detail.quantity]:
                    models.OrderDetails.objects.create(order=order, laptop=laptop, price=model.price)
                    # SOLD LAPTOP.
                    laptop.is_sold = True
                    laptop.save()
                # REDUCE QUANTITY.
                model.quantity -= detail.quantity
                model.save()
        # DELETE ALL CART DETAILS.
        details.delete()
        sessions.add(request, 'Thao tác thành công', 'Đặt hàng thành công')
    else:
        sessions.add(request, 'Thanh toán thất bại', 'Giỏ hàng đang trống', False)

    return redirect('orders:cart-page', permanent=True)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
@atomic
def cancel_order(request: HttpRequest, pk: int):
    # TRANSFORM STATE OF ORDER.
    order = get_object_or_404(models.Order, pk=pk)
    order.state = models.State.objects.get(pk=5)
    order.save()
    # RE-SOLD LAPTOP & RE-INCREASE QUANTITY OF MODEL.
    for laptop in order.laptops.all():
        laptop.is_sold = False
        laptop.laptop_model.quantity += 1
        laptop.laptop_model.save()
        laptop.save()

    sessions.add(request, 'Thao tác thành công', 'Đơn hàng đã được hủy')
    return redirect('orders:order-page', 0)


# CART.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def cart_page(request: HttpRequest):
    customer = request.user.customer
    addresses = customer.deliveryaddress_set.all()
    cart_models = customer.cart_details.all()
    cart_details = CartDetails.objects.filter(customer=customer)
    total = sum(map(lambda e: e.quantity * e.laptop_model.price * (e.laptop_model.quantity > 0), cart_details))

    context = {'cart_models': cart_models, 'cart_details': cart_details,
               'total': total, 'addresses': addresses, **sessions.get(request)}
    return render(request, 'orders/cart.html', context)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def create_cart(request: HttpRequest, pk: int):
    customer = request.user.customer
    model = get_object_or_404(LaptopModel, pk=pk)
    # CHECK EXIST.
    cart_detail = CartDetails.objects.filter(customer=customer, laptop_model__pk=pk).first()
    if cart_detail:
        if cart_detail.quantity < model.quantity:
            cart_detail.quantity += 1
            cart_detail.save()
    else:
        CartDetails.objects.create(laptop_model=model, customer=customer, quantity=1)
    sessions.add(request, 'Thao tác thành công', 'Hãy kiểm tra giỏ hàng')

    return redirect('orders:product', pk)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def update_cart(request: HttpRequest, pk: int):
    cart_detail = get_object_or_404(CartDetails, pk=pk)
    # INCREASE/DECREASE.
    quantity = cart_detail.quantity + int(request.GET.get('control'))
    if quantity <= cart_detail.laptop_model.quantity:
        # DELETE IF QUANTITY EQUALS TO ZERO.
        if quantity == 0:
            cart_detail.delete()
        else:
            cart_detail.quantity = quantity
            cart_detail.save()
    # ERROR MESSAGE IF QUANTITY IS OVER THE INVENTORY.
    else:
        sessions.add(request, 'Thao tác thất bại', 'Không thể vượt quá số lượng hiện có', False)

    return redirect('orders:cart-page')


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def delete_cart(request: HttpRequest, pk: int):
    cart_detail = get_object_or_404(CartDetails, pk=pk)
    cart_detail.delete()

    return redirect('orders:cart-page')


# PRODUCT.
def product_detail(request: HttpRequest, pk: int):
    model = get_object_or_404(LaptopModel, pk=pk)
    cart_models = request.user.customer.cart_details.all() if request.user.is_authenticated else None

    context = {'model': model, 'cart_models': cart_models, **sessions.get(request)}
    return render(request, 'orders/product.html', context)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
@atomic
def buy_now(request: HttpRequest):
    # GET DATA.
    customer = request.user.customer
    fullname = request.POST.get('HoTen')
    phone = request.POST.get('sdt')
    address = request.POST.get('diaChi')
    delivery_address = f'{fullname}, {phone}, {address}'
    # GET LAPTOP.
    model_id = int(request.POST.get('model'))
    model = LaptopModel.objects.get(pk=model_id)
    laptop = model.laptop_set.filter(is_sold=False).first()
    # CREATE ORDER.
    order = models.Order.objects.create(customer=customer, address=delivery_address)
    # CREATE ORDER DETAIL.
    models.OrderDetails.objects.create(order=order, laptop=laptop, price=model.price)
    # REDUCE QUANTITY.
    model.quantity -= 1
    model.save()
    # SOLD LAPTOP.
    laptop.is_sold = True
    laptop.save()

    return redirect('orders:order-page', 0)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def purchase_cart(request: HttpRequest, pk: int):
    customer = request.user.customer
    model = get_object_or_404(LaptopModel, pk=pk)
    # CHECK EXIST.
    cart_detail = CartDetails.objects.filter(customer=customer, laptop_model__pk=pk).first()
    if cart_detail:
        if cart_detail.quantity < model.quantity:
            cart_detail.quantity += 1
            cart_detail.save()
    else:
        CartDetails.objects.create(laptop_model=model, customer=customer, quantity=1)

    return redirect('orders:cart-page')
