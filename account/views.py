from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('product:home')
        else:
            return render(request, 'account/login.html',{'error':'username or password is incorrect.'})
    else:
        return render(request, 'account/login.html')

def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['password-re']:
            try:
                user = User.objects.get(username = request.POST['username'])
                return render(request, 'account/signup.html', {'error':'username is already taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                auth.login(request,user)
                return redirect('product:home')
        else:
            return render(request, 'account/signup.html', {'error':'Passwords must match'})
    else:
        return render(request, 'account/signup.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('account:login')
