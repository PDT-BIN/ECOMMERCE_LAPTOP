from webapps import sessions
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
# DATA.
from django.db.transaction import atomic
from orders.models import DeliveryAddress
from .models import User, Customer
from .forms import SignInForm, SignUpForm, PersonalForm
# TOKEN.
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import ACCOUNT_ACTIATION_TOKEN
# PERMISSION.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.decorators import user_passes_test
# CHATBOT.
import json
from Chatbot import ChatBot
import csv
from googletrans import Translator


def check_customer_permission(user: AbstractBaseUser) -> bool:
    return user.is_authenticated and not (user.is_superuser or user.is_staff or user.is_shipper)


# LOGIN, SIGNUP & LOGOUT.
@atomic
def signup_page(request: HttpRequest):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # CREATE USER.
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Customer.objects.create(user=user)
            # SEND MAIL.
            ACCOUNT_ACTIATION_TOKEN.send_email(request, user, 'Activate your account', 'email/verification.html')
            # SUCCESS.
            sessions.add(request, 'Đăng ký thành công', 'Hãy kiểm tra email của bạn')
            return redirect('signin')
        else:
            # FAILURE.
            sessions.add(request, 'Đăng ký thất bại', 'Thông tin không hợp lệ', False)

    context = {'form': form, **sessions.get(request)}
    return render(request, 'signup.html', context)


def activate(request: HttpRequest, uidb64: str, token: str):
    # GET DATA FROM TOKEN.
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    # VERIFY USER.
    if user and ACCOUNT_ACTIATION_TOKEN.check_token(user, token):
        user.is_active = True
        user.save()
        # SUCCESS.
        sessions.add(request, 'Xác thực thành công', 'Tài khoản của bạn đã được xác thực')
        return redirect('signin')
    else:
        # FAILURE.
        return render(request, 'email/failed_verify.html')


def signin_page(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('home')

    form = SignInForm(request)
    if request.method == 'POST':
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            sessions.add(request, 'Đăng nhập thất bại', 'Thông tin không chính xác', False)

    context = {'form': form, **sessions.get(request)}
    return render(request, 'signin.html', context)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def logout_page(request: HttpRequest):
    logout(request)
    return redirect('signin')


# FORGOT PASSWORD.
def forgot_page(request: HttpRequest):
    if request.method == 'POST':
        # GET DATA.
        username = request.POST.get('username')
        email = request.POST.get('email')
        # VERIFY USER..
        user = User.objects.filter(username=username, email=email).first()
        if user:
            # SEND MAIL.
            ACCOUNT_ACTIATION_TOKEN.send_email(request, user, 'Reset your password', 'email/reset_password.html')
            # SUCCESS.
            sessions.add(request, 'Thao tác thành công', 'Hãy kiểm tra email của bạn')
            return redirect('signin')
        else:
            # FAILURE.
            sessions.add(request, 'Thao tác thất bại', 'Thông tin không chính xác', False)

    return render(request, 'forgot.html')


def reset_password(request: HttpRequest, uidb64: str, token: str):
    # GET DATA FROM TOKEN.
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    # VERIFY USER.
    if user and ACCOUNT_ACTIATION_TOKEN.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 == password2:
                user.set_password(password1)
                user.save()
                # SUCCESS.
                sessions.add(request, 'Thao tác thành công', 'Khôi phục mật khẩu thành công')
                return redirect('signin')
            else:
                # FAILURE.
                sessions.add(request, 'Thao tác thất bại', 'Mật khẩu xác nhận không trùng khớp', False)
    else:
        # FAILURE.
        return render(request, 'email/failed_verify.html')

    return render(request, 'reset.html', {**sessions.get(request)})


# PROFILE PAGE.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def profile_page(request: HttpRequest, choice: int):
    customer = request.user.customer
    cart_models = customer.cart_details.all()
    # INFORMATION
    form = PersonalForm(instance=customer)
    # ADDRESS.
    addresses = customer.deliveryaddress_set.all()

    context = {'form': form, 'choice': choice, 'addresses': addresses,
               'cart_models': cart_models, **sessions.get(request)}
    context.update({'addresses': addresses} if choice == 2 else {})
    return render(request, 'profile.html', context)


# INFORMATION.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def update_profile(request: HttpRequest):
    form = PersonalForm(instance=request.user.customer, data=request.POST)
    if form.is_valid():
        form.save()
        sessions.add(request, 'Thao tác thành công', 'Cập nhật thông tin thành công')

    return redirect("profile", 1)


# PASSWORD.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def change_password(request: HttpRequest):
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

    return redirect("profile", 4)


# ADDRESS.
@user_passes_test(test_func=check_customer_permission, login_url='signin')
def create_or_update_address(request: HttpRequest):
    fullname = request.POST.get('fullname')
    phone = request.POST.get('phone')
    number = request.POST.get('number')
    province, district, communce = request.POST.get(
        'province'), request.POST.get('district'), request.POST.get('commune')
    address = (f'{number}, ' if number else '') + f'{communce}, {district}, {province}'

    customer = request.user.customer
    if (pk := int(request.POST.get("pk"))) == -1:
        DeliveryAddress.objects.create(
            fullname=fullname, phone=phone, address=address, customer=customer)
    else:
        DeliveryAddress.objects.filter(pk=pk).update(
            fullname=fullname, phone=phone, address=address, customer=customer)

    return redirect('profile', 2)


@user_passes_test(test_func=check_customer_permission, login_url='signin')
def delete_address(request: HttpRequest):
    address = get_object_or_404(DeliveryAddress, pk=request.POST.get('pk'))
    address.delete()
    return redirect('profile', 2)


# CHATBOT.
def chatting(request: HttpRequest):
    data = json.loads(request.body)
    message = data.get('message', '')
    context=""
    if request.session.get('context') != None:
        context = request.session.get('context')
    response = ChatBot.chat(message, context)
    if response[2]!="":
        request.session['context'] = response[2]
    if request.session.get('chat') == None:
        request.session['chat'] = [[message, response]]
    else:
        chat = request.session.get('chat')
        chat.append([message, response])
        request.session['chat'] = chat
    response_data = json.dumps(response)
    return HttpResponse(response_data, content_type='json')


def getChat(request: HttpRequest):
    if request.session.get('chat') == None:
        chat=[]
    else:
        chat = request.session.get('chat')
    response_data = json.dumps(chat)
    return HttpResponse(response_data, content_type='json')


def thumbsup(request: HttpRequest):
    data = json.loads(request.body)
    translator = Translator()
    message = translator.translate(data.get('message', '')).text
    label = data.get('label', '')
    if label =="":
        response_data = json.dumps("")
        return HttpResponse(response_data, content_type='json')
    labelExist=False
    with open("Chatbot/record/understand.json") as file:
        data = json.load(file)
    for intent in data["intents"]:
        if intent["tag"] == label:
            if message not in intent["patterns"]:
                intent["patterns"].append(message)
                labelExist=True
    if not labelExist:
        dictd={
            "tag": label,
            "patterns": [
                message
            ],
        }
        data["intents"].append(dictd)
    with open("Chatbot/record/understand.json", "w") as file:
        json.dump(data, file)

    response_data = json.dumps("")
    return HttpResponse(response_data, content_type='json')


def thumbsdown(request: HttpRequest):
    data = json.loads(request.body)
    translator = Translator()
    message = translator.translate(data.get('message', '')).text
    f = open('Chatbot/record/misunderstand.csv', 'a', newline='', encoding="utf-8")
    csvwt = csv.writer(f)
    csvwt.writerow([message])
    f.close()
    response_data = json.dumps("")
    return HttpResponse(response_data, content_type='json')
