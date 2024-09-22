from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import CustomUser as User
from django.conf import settings
import secrets
from .redis import r
from .tasks import send_register_email, send_reset_password_email
from django.core.mail import send_mail


def login(request):
    if request.method == 'GET':
        form = CustomLoginForm()
        return render(request, 'users/login.html', {'form': form})
    elif request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth_login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(next)
                return redirect('home')
        return redirect('login')


def register(request):
    if request.method == 'GET':
        return render(request, 'users/register/step1.html')
    elif request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if not user:
            hash = secrets.token_hex(32)
            r.set(hash, email, ex=300)
            url = f'{settings.URL}users/register/verified?hash={hash}'
            users = [email]
            message = f'''Для продолжения регистрации перейдите по ссылке:
            {url}
            '''
            send_register_email.delay(message, users)

            return redirect(f"{reverse('email-success')}?email={email}")
        else:
            return render(request, 'users/register/step1.html', {'error': 'Аккаунт с такой почтой уже существует'})
def password_reset(request):
    if request.method == 'GET':
        return render(request, 'users/reset-password.html')
    elif request.method == 'POST':
        username = request.POST['login']
        email = request.POST['email']
        user = User.objects.filter(email=email).filter(username=username).first()
        if not user:
            return render(request, 'users/reset-password.html', {'error': 'Аккаунт не найден'})
        hash = secrets.token_hex(32)
        r.set(f'{hash}-reset-password', user.id, ex=420)
        print(f'{hash}-reset-password')
        url = f'{settings.URL}users/password-reset/verified?hash={hash}'
        users = [email]
        message = f'''Для сброса пароля перейдите по ссылке:
        {url}'''
        send_reset_password_email(message, users)
        return render(request, 'users/reset-password.html', {'success': f'Ссылка для продолжения отправлена на {email}'})

def password_reset_verified(request):
    if request.method == 'GET':
        hash = request.GET.get('hash')
        if r.get(f'{hash}-reset-password'):
            user_id = r.get(f'{hash}-reset-password')
        else:
            return HttpResponse('Отказано')
        user = User.objects.get(id=user_id)
        if user:
            return render(request, 'users/reset-password-step2.html',{'hash': hash})
    elif request.method == "POST":
        hash = request.POST.get('hash')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'users/reset-password-step2.html', {'error':'Пароли не совпадают'})
        user_id = r.get(f'{hash}-reset-password')
        if not user_id:
            return render(request, 'users/reset-password-step2.html', {'error': 'Время сессии истекло, попробуйте снова'})
        user = User.objects.filter(id=user_id).first()
        user.set_password(password1)
        user.save()
        r.delete(f'{hash}-reset-password')
        return redirect('login')


    else:
        return HttpResponse('Отказано')
def email_success(request):
    email = request.GET.get('email')
    return render(request, 'users/register/step1-success.html', {'email': email})

def register_verified(request):
    if request.method == 'GET':
        hash = request.GET.get('hash')
        email = r.get(hash)
        if email:
            return render(request, 'users/register/step2.html', {'email': email})
        else:
            return HttpResponse('Отказано в доступе')
    elif request.method == 'POST':
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat_password')
        email = request.POST.get('email')
        if password != repeat_password:
           return render(request, 'users/register/step2.html', {'email': email, 'error': 'Пароль должен быть одинаковый в обоих полях'})
        username = request.POST.get('login')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if email and username and first_name and last_name and password:
           user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
           user.save()
           auth_login(request, user)
           return redirect('home')
        print(email, username, first_name, last_name, password, repeat_password)
        return render(request, 'users/register/step2.html', {'email': email})


def exit(request):
    logout(request)
    return redirect('home')