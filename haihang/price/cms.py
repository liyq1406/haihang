# -*- coding:utf-8 -*-

import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Price
from django import forms
from django.http import HttpResponseRedirect
from Payment.util import get_kwargs
from django.forms.models import model_to_dict


log = logging.getLogger('payment')

class AccountForm(forms.Form):
    credit = forms.IntegerField(required=False, min_value=0)
    balance = forms.IntegerField(required=False, min_value=0)
    user_uuid = forms.UUIDField()

@login_required
def create_account(request):
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account = PaymentAccount(**get_kwargs(account_form.cleaned_data))
            account.save()
            log.info("[account] payment account %s create success", account.payment_account_uuid)
            return HttpResponseRedirect('/cms/price/?page=1')
        else:
            data = {
                'account_form': account_form,
                'mode': u'create'
            }
            log.info("bad request")
            return render(request, 'account_edit.html', data)
    else:
        data = {
            'account_form': AccountForm(),
            'mode': u'create'
        }
    return render(request, 'account_edit.html', data)

@login_required
def edit_account(request, pk=None):
    try:
        account = PaymentAccount.objects.get(payment_account_uuid=pk)
    except PaymentAccount.DoesNotExist:
        log.error('[account] no such payment account %s', uuid)
        return HttpResponseRedirect('/cms/account/?page=1')
    if request.method == 'POST':
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account.credit = account_form.cleaned_data['credit']
            account.balance = account_form.cleaned_data['balance']
            account.save()
            log.info("[account] payment account %s edit success", account.payment_account_uuid)
            return HttpResponseRedirect('/cms/account/?page=1')
        else:
            data = {
                'account_form': account_form,
                'mode': u'edit'
            }
            log.info("bad request")
            return render(request, 'account_edit.html', data)
    else:
        init_attr = model_to_dict(account)
        data = {
            'account_form': AccountForm(initial=init_attr),
            'mode': u'edit'
        }
    return render(request, 'account_edit.html', data)

@login_required
def list_price(request):
    search = request.GET.get('search')
    if search:
        price_list = PaymentAccount.objects.filter(payment_account_uuid=search).order_by('-create_time')
    else:
        price_list = Price.objects.all().order_by('-created')
    paginator = Paginator(price_list, 10)

    page = request.GET.get('page')
    try:
        prices = paginator.page(page)
    except PageNotAnInteger:
        prices = paginator.page(1)
    except EmptyPage:
        prices = paginator.page(paginator.num_pages)
    page_info = {
        'pre': prices.has_previous(),
        'next': prices.has_next()
    }
    return render(request, 'price_list.html', {"accounts": prices, 'page_info': page_info})

@login_required
def list_account_record(request, pk):
    record_list = AccountRecord.objects.filter(payment_account_uuid=pk)
    paginator = Paginator(record_list, 10)

    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    page_info = {
        'pre': records.has_previous(),
        'next': records.has_next(),
        'account': pk
    }
    return render(request, 'account_record_list.html', {"records": records, 'page_info': page_info})
