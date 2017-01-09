# -*- coding:utf-8 -*-

import logging
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Reconciliation


log = logging.getLogger('payment')

@login_required
def list_reconciliation(request):
    search = request.GET.get('search')
    if not search:
        reconciliation_list = Reconciliation.objects.all().order_by('-create_time')
    else:
        reconciliation_list = Reconciliation.objects.filter(payment_no=search).order_by('-create_time')

    paginator = Paginator(reconciliation_list, 10) 

    page = request.GET.get('page')
    try:
        reconciliations = paginator.page(page)
    except PageNotAnInteger:
        reconciliations = paginator.page(1)
    except EmptyPage:
        reconciliations = paginator.page(paginator.num_pages)
    page_info = {
        'pre': reconciliations.has_previous(),
        'next': reconciliations.has_next()
    }
    return render(request, 'reconciliation_list.html', {"reconciliations": reconciliations, 'page_info': page_info})
