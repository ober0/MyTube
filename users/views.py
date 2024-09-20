from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import CustomUser as User
from django.conf import settings
import secrets
from .redis import r
from .tasks import send_register_email
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
            url = f'{settings.URL}/users/register/verified?hash={hash}'
            users = [email]
            message = f'''Для продолжения регистрации перейдите по ссылке:
            {url}
            '''

            send_register_email.delay(message, users)

            return redirect(f"{reverse('email-success')}?hash={hash}")
        else:
            return JsonResponse({
                'success': False,
                'error': 'Пользователь с этим email-ом уже существует. '
            })
def password_reset(request):
    return HttpResponse(f'<h1>success</h1>')

def email_success(request):

    return HttpResponse()