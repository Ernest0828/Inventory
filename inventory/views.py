from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect

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

def protected_view(request): 
    user = request.user
    if not user.is_authenticated:
        return redirect('/login/')
          
    df = pd.read_excel('C:/Users/ErnestKhong/Cable Coatings Limited t a AssetCool/AssetCool - Data Analysis/Engineering/inventory_control/Master Inventory.xlsx', sheet_name = 'BRP (Mark 1 + 1.5 + 2)')
    # item_name = df['Item name']
    # item_id = df['Item ID']
    # stock = df['Stock']
    data = df[['Item name', 'Item ID', 'Stock']].to_dict(orient='records')
    cleaned_data = []
    for row in data:
        cleaned_row = {
            'item_name': row['Item name'],
            'item_id': row['Item ID'],
            'stock': row['Stock']
        }
        if pd.isna(cleaned_row['item_id']):
            cleaned_row['item_id'] = "nan"
        cleaned_row['stock'] = int(cleaned_row['stock']) if not pd.isna(cleaned_row['stock']) else 0

        cleaned_data.append(cleaned_row)

    out_of_stock = sum(1 for item in cleaned_data if item['stock'] == 0)
    context = {
        'data': cleaned_data,
        'out_of_stock': out_of_stock,
    }

    return render(request, 'pages/inventory.html', context)

