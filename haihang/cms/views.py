# -*- coding:utf-8 -*-
import logging
from django.shortcuts import render
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

log = logging.getLogger('payment')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
    def clean(self):
        usr = self.cleaned_data['username']
        pwd = self.cleaned_data['password']
        user = authenticate(username=usr, password=pwd)
        if not user:
            raise forms.ValidationError(u'用户名或密码错误!')
        return self.cleaned_data

def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            log.info("user %s login success", user.username)
            return HttpResponseRedirect('/cms/account/?page=1')
        else:
            log.info("user login auth fail")
            return render(request, 'login.html', {'login_form': login_form})
    else:
        logout(request)
        login_form = LoginForm()
    return render(request, 'login.html', {'login_form': login_form})

# @login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/cms/login/')
