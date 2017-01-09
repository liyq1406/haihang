# -*- coding:utf-8 -*-

import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Payment, PaymentRecord, PaymentRefund


log = logging.getLogger('payment')

@login_required
def list_payment(request):
    search = request.GET.get('search')
    if search:
        payment_list = Payment.objects.filter(payment_uuid=search).order_by('-create_time')
    else:
        payment_list = Payment.objects.all().order_by('-create_time')

    paginator = Paginator(payment_list, 10) 

    page = request.GET.get('page')
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)
    page_info = {
        'pre': payments.has_previous(),
        'next': payments.has_next()
    }
    return render(request, 'payment_list.html', {"payments": payments, 'page_info': page_info})

@login_required
def list_payment_record(request, pk):
    record_list = PaymentRecord.objects.filter(payment_uuid=pk)
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
        'payment': pk
    }
    return render(request, 'payment_record_list.html', {"records": records, 'page_info': page_info})

@login_required
def detail_payment(request, pk):
    payment = Payment.objects.get(pk=pk)
    return render(request, 'payment_detail.html', {"payment": payment})

@login_required
def list_payment_refund(request):
    search = request.GET.get('search')
    if search:
        refund_list = PaymentRefund.objects.filter(payment_uuid=search).order_by('-create_time')
    else:
        refund_list = PaymentRefund.objects.all().order_by('-create_time')

    paginator = Paginator(refund_list, 10) 

    page = request.GET.get('page')
    try:
        refunds = paginator.page(page)
    except PageNotAnInteger:
        refunds = paginator.page(1)
    except EmptyPage:
        refunds = paginator.page(paginator.num_pages)
    page_info = {
        'pre': refunds.has_previous(),
        'next': refunds.has_next()
    }
    return render(request, 'payment_refund_list.html', {"refunds": refunds, 'page_info': page_info})
