# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View

from .models import UserProfile
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password

# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # “Q|Q”表示或，并 "Q，Q"表示and
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form1": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.password = make_password(pass_word)
            user_profile.save()
            pass


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "输入用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})
