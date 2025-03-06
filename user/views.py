from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login Successful!!')

            next_url = request.GET.get('next', 'post_list')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Aaaaa')
        
    return render(request, 'user/login.html')


def user_logout(request):
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect('dashboard')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            messages.error(request, "Password do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username Already Exists.')
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email Already Used to create account.')
            return redirect('signup')
        
        if email=='' or username == '' or password == '':
            messages.error(request, 'Fields cannot be empty.')
            return redirect('signup')
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)
        messages.success(request, "Signup successful!!")
        return redirect('post_list')
    
    return render(request, 'user/signup.html')