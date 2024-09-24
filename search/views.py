from django.shortcuts import render, HttpResponse, redirect

def search_main(request):
    if request.method == 'GET':
        par = request.GET.get('par')
        if par is None:
            par = ''
        return HttpResponse(par)
