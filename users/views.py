from django.http import HttpResponse
from django.shortcuts import render, redirect

def login(request):
    if request.method == 'GET':
        return render(request, 'users/login.html')
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['pass']
        print(email, password)
        return redirect('home')
def register(request):
    return HttpResponse('<h1>страница в разработке</h1>')

def password_reset(request):
    return HttpResponse('<h1>страница в разработке</h1>')