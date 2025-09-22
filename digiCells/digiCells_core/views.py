from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import LoginForm



def index(request):
    return render(request, 'home.html')


def login_request(request):

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('index')
        else:
            login_form.add_error(None, 'Invalid login details')
    else:
        login_form = LoginForm()
    return render(request, 'user/login.html', {'login_form': login_form})


def logout_request(request):
    logout(request)
    messages.success(request, "you have successfully logged out")
    return redirect("login")
