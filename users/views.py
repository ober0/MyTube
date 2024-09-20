from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomLoginForm
from django.contrib.auth import authenticate, login as auth_login, logout


def login(request):
    if request.method == 'GET':
        form = CustomLoginForm()
        print(form)
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
    return HttpResponse('<h1>страница в разработке</h1>')

def password_reset(request):
    return HttpResponse('<h1>страница в разработке</h1>')