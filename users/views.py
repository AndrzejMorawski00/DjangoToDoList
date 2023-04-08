import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def login_user(request):
    errors = []
    if request.user.is_authenticated:
        return redirect("todo:home-view")
    else:
        if request.method == "POST":
            username = request.POST['username']
            user_password = request.POST['password']
            user = authenticate(username=username, password=user_password)
            if user is None:
                errors.append("Something went wrong, try again")
                return render(request, "users/login.html", {"errors": errors})
            else:
                login(request, user)
                return redirect("todo:home-view")

        else:
            return render(request, "users/login.html", {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("todo:home-view")


def register_user(request):
    errors = []
    if request.user.is_authenticated:
        return redirect("todo:home-view")
    else:
        if request.method == "POST":
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                username = register_form.cleaned_data['username']
                password = register_form.cleaned_data['password1']
                user = authenticate(username=username, password=password)
                if user is None:
                    errors.append("Something went wrong, try again")
                    return render(request, "users/register.html", {"register_form": register_form, "errors": errors})
                else:
                    login(request, user)
                    return redirect("todo:home-view")
            else:
                print(register_form.errors)
                for error in register_form.errors:
                    error_message = re.split(
                        '<li>|</li>', str(register_form.errors[error]))[1]
                    errors.append(error_message)

                return render(request, "users/register.html", {"register_form": register_form, "errors": errors})
        else:
            register_form = RegisterForm()
            return render(request, "users/register.html", {"register_form": register_form})
