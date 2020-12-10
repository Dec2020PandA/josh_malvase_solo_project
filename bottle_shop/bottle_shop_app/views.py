from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User

## RENDER
def log_reg(request):
    return render(request, "log_reg.html")
def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')
    return render(request, 'profile.html')    

## LOG AND REG
def login(request):
    if request.method=="POST":
        if not User.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email/Password')
            return redirect('/')
        logged_user = User.objects.filter(email=request.POST['email'])
        if logged_user:
            logged_user=logged_user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id']=logged_user.id
                request.session['user_name']=f"{logged_user.first_name} {logged_user.last_name}"
                return redirect('/mybottleshop')
    return redirect('/')
def register(request):
    if request.method=='POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        user_pw = request.POST['password']
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        print(hash_pw)
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], username =request.POST['username'], email=request.POST['email'], password=hash_pw)
        print(new_user)
        request.session['user_id']=new_user.id
        request.session['full_name']=f"{new_user.first_name} {new_user.last_name}"
        request.session['username']=new_user.username
        return redirect('/mybottleshop')
    return redirect('/')

## LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')

