from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from .forms import LoginForm


def index(request):
    return render(request, "home.html")


def login_request(request):

    if request.method == "POST":
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("index")
        else:
            login_form.add_error(None, "Invalid login details")
    else:
        login_form = LoginForm()
    return render(request, "user/login.html", {"login_form": login_form})


def logout_request(request):
    logout(request)
    messages.success(request, "you have successfully logged out")
    return redirect("login")


@csrf_exempt
def csrf_debug(request):
    """Debug view to help troubleshoot CSRF issues"""
    if request.method == "GET":
        csrf_token = get_token(request)
        return JsonResponse(
            {
                "csrf_token": csrf_token,
                "method": request.method,
                "is_secure": request.is_secure(),
                "host": request.get_host(),
                "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                "referer": request.META.get("HTTP_REFERER", ""),
            }
        )
    return JsonResponse({"error": "Only GET requests allowed"})
