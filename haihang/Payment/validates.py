# -*- coding:utf-8 -*-

from django.core.exceptions import ValidationError
from rest_framework import serializers

def non_negative(value):
    if value < 0:
        raise ValidationError('%f is not a non-negative' % value)

def in_range(value):
    if value < 1 or value > 1000:
        raise serializers.ValidationError(u'coupon_count should between 1 and 1000')

def positive(value):
    if value < 1:
        raise ValidationError('%f is not a positive integer' % value)

def is_digit(value):
    if not value.isdigit():
        raise ValidationError('%s is not a valid integer' % value)