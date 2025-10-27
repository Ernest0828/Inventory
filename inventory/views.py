from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from .models import Items
import openpyxl

# Create your views here.
def register_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']       
    except:
        return Response('Invalid Data', status=400)
        #if email doesnt end with @assetcool.com, return error
    if not email.endswith('@assetcool.com'):
        return Response('Email must be an @assetcool.com email', status=400)
    if User.objects.filter(username=username).exists():
        return Response('Username already exists', status=400)
    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    return Response('User created successfully', status=201)

def login_view(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
        except:
            return HttpResponse('Invalid Data', status=400)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/view/')
        else:
            return HttpResponse('Invalid credentials', status=400)
    else:
        return render(request, 'pages/login.html')
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'pages/logout.html')
    else:
        return HttpResponse('Not logged in', status=400)

def inventory_view(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')

    all_items = Items.objects.all()
    out_of_stock = Items.objects.filter(stock=0).count()

    data = []
    for item in all_items:
        data.append({
            'item_name': item.item_name,
            'item_id': item.item_id,
            'stock': item.stock
        })
    
    context = {
        'data': data,
        'out_of_stock': out_of_stock,
    }

    return render(request, 'pages/inventory.html', context)

