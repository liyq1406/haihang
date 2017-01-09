# -*- coding:utf-8 -*-

import logging, string, random
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Coupon, CouponUsage
from django import forms
from django.http import StreamingHttpResponse
from Payment.initConf import MODULE_COUPON
from django.db.transaction import TransactionManagementError

log = logging.getLogger('payment')

COUPON_TYPE = (
    ('discount', 'discount'),
    ('reduce', 'reduce'),
    ('recharge', 'recharge'),
)

class CouponForm(forms.Form):
    coupon_type = forms.ChoiceField(choices=COUPON_TYPE)
    coupon_value = forms.IntegerField(min_value=1)
    coupon_using_count = forms.IntegerField(min_value=0)
    coupon_using_user = forms.IntegerField(min_value=0)
    valid_datetime_start = forms.DateTimeField()
    valid_datetime_end = forms.DateTimeField()
    coupon_count = forms.IntegerField(min_value=1, max_value=1000)

@login_required
def create_coupon(request):
    if request.method == 'POST':
        coupon_form = CouponForm(request.POST)
        if coupon_form.is_valid():
            queryset = Coupon.objects.all()
            chars = string.uppercase + string.digits
            code_list_temp = []
            code_list_valid = []
            create_count = coupon_form.cleaned_data['coupon_count']
            while len(code_list_valid) < create_count:
                s = [random.choice(chars) for i in range(MODULE_COUPON['COUPON_CODE_LEN'])]
                code = ''.join(s)
                if code not in code_list_temp and queryset.filter(coupon_code=code).count()==0:
                    code_list_valid.append(code)
                code_list_temp.append(code)
            coupon_path = ''.join(['data/coupon/', str(time.time()).replace('.','_'), '.txt'])
            coupon_type = coupon_form.cleaned_data['coupon_type']
            coupon_using_count = coupon_form.cleaned_data['coupon_using_count']
            coupon_using_user = coupon_form.cleaned_data['coupon_using_user']
            valid_datetime_start = coupon_form.cleaned_data['valid_datetime_start']
            valid_datetime_end = coupon_form.cleaned_data['valid_datetime_end']
            coupon_value = coupon_form.cleaned_data['coupon_value']
            try:
                f = open(coupon_path, 'wb')
                for code in code_list_valid:
                    f.write(code + '\n')
                    coupon = Coupon(coupon_code=code, coupon_type=coupon_type, 
                                    coupon_using_count=coupon_using_count,
                                    coupon_using_user=coupon_using_user,
                                    using_user_left=coupon_using_user,
                                    valid_datetime_start=valid_datetime_start,
                                    valid_datetime_end=valid_datetime_end,
                                    coupon_value=coupon_value)
                    coupon.save()
                f.close()
                log.info('[coupon] create %d coupon codes at %s.',create_count, coupon_path)
            except IOError:
                log.error('[coupon] write file %s fail', coupon_path)
            except TransactionManagementError:
                log.error('[coupon] create coupon error ')
            data = {
                'coupon_form': coupon_form,
                'coupon_path': coupon_path.replace('data/coupon/', '')
            }
            return render(request, 'coupon_create.html', data)
        else:
            log.info("bad request")
            return render(request, 'coupon_create.html', {'coupon_form': coupon_form})
    else:
        return render(request, 'coupon_create.html', {'coupon_form': CouponForm()})

# @login_required
def download_coupon(request):
    target = request.GET.get('target')
    coupon_path = 'data/coupon/' + target
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(coupon_path))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(target)
    log.info('[coupon] gen download coupon file %s success', target)
    return response

@login_required
def list_coupon(request):
    search = request.GET.get('search')
    if not search:
        coupon_list = Coupon.objects.all().order_by('-create_time')
    elif len(search)==8:
        coupon_list = Coupon.objects.filter(coupon_code=search).order_by('-create_time')
    else:
        coupon_list = Coupon.objects.filter(coupon_uuid=search).order_by('-create_time')

    paginator = Paginator(coupon_list, 10) 

    page = request.GET.get('page')
    try:
        coupons = paginator.page(page)
    except PageNotAnInteger:
        coupons = paginator.page(1)
    except EmptyPage:
        coupons = paginator.page(paginator.num_pages)
    page_info = {
        'pre': coupons.has_previous(),
        'next': coupons.has_next()
    }
    return render(request, 'coupon_list.html', {"coupons": coupons, 'page_info': page_info})

@login_required
def list_coupon_record(request, pk):
    record_list = CouponUsage.objects.filter(coupon_uuid=pk)
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
        'coupon': pk
    }
    return render(request, 'coupon_record_list.html', {"records": records, 'page_info': page_info})
