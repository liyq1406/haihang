# -*- coding:utf8 -*-
from price.models import Price, PriceAddRecord
from price.serializers import PriceSerializer, RecordPriceSerializer
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import list_route
from django.shortcuts import get_object_or_404
import datetime
import logging
import pytz
from Payment.disable import CsrfExemptSessionAuthentication, auth_required

log = logging.getLogger('payment')


def gain_price_obj(args):
    """
    args为一个元祖，里面有cpu,mem,disk
    :param args:
    :return:
    """
    current_date = datetime.datetime.now()
    price_obj = Price.objects.filter(cpu=args[0], mem=args[1], disk=args[2], effective_date__lte=current_date). \
        order_by('-effective_date')
    if price_obj.count() == 0:
        return False
    else:
        return price_obj[0]


class PriceViewSet(mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    根据容器配置条件查看定价
    cpu:cpu核数 int
    mem:内存大小
    disk：磁盘大小
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    @auth_required(role='superadmin')
    @list_route(methods=['post'])
    def create_price(self, request):
        try:
            cpu = request.data.get('cpu')
            mem = request.data.get('mem')
            disk = request.data.get('disk')
            price = request.data.get('price')
            host_model = request.data.get('host_model')
            is_existed = request.data.get('is_existed')
            effective_date = request.data.get('effective_date')
            tz = pytz.timezone('Asia/Shanghai')
            log.info('[price] create_price.effective_date:%s', effective_date)
            effective_date = datetime.datetime.strptime(effective_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            effective_date = (effective_date + datetime.timedelta(hours=8)).date().replace(day=1)
            log.info('[price] create_price.effective_date Asia/Shanghai:%s', effective_date)
            if price <= 0 or cpu <= 0 or mem <= 0 or disk <= 0:
                return Response({'detail': 'the value error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
            if effective_date < datetime.datetime.now(tz).date():
                return Response({'detail': 'the effective_data error.', 'error_code': '6400'},
                                status=status.HTTP_400_BAD_REQUEST)

            price_check = Price.objects.filter(host_model=host_model)
            if price_check.count() == 1:
                return Response({'detail': 'this price host_model is existed.', 'error_code': '6400'},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                price_new = Price(cpu=cpu, mem=mem, disk=disk, price=price, host_model=host_model,
                                  effective_date=effective_date, is_existed=is_existed)
                price_new.save()
                record_new = PriceAddRecord(price_uuid=price_new.price_uuid,
                                            action='add a new price,price=' + str(price))
                record_new.save()
            return Response({'sattus': 'create price success'})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            log.error('[price] veiws.create_price.e:{}'.format(e.__str__()))
            return Response({'detail': 'other error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='superadmin')
    @list_route(methods=['post'])
    def add_type_price(self, request):
        try:
            host_model = request.data.get('host_model')
            price = request.data.get('price')
            is_existed = request.data.get('is_existed')
            effective_date = request.data.get('effective_date')
            log.info('[price] views.add_type_price effective_date:%s', effective_date)
            tz = pytz.timezone('Asia/Shanghai')
            effective_date = datetime.datetime.strptime(effective_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            effective_date = (effective_date + datetime.timedelta(hours=8)).date().replace(day=1)
            log.info('[price] add_type_price effective_date:%s', effective_date)
            check_name = Price.objects.filter(host_model=host_model)
            if effective_date < datetime.datetime.now(tz).date():
                return Response({'detail': 'the effective_date is error.', 'error_code': '6400'},
                                status=status.HTTP_403_FORBIDDEN)
            if check_name.count() == 0:
                return Response({'detail': 'no the host_model price.', 'error_code': '6400'},
                                status=status.HTTP_403_FORBIDDEN)
            for _ in check_name:
                if _.effective_date == effective_date:
                    return Response({'detail': 'the effective_date is conflict', 'error_code': '6403'},
                                    status=status.HTTP_403_FORBIDDEN)
            if price < 0:
                return Response({'detail': 'the price should bigger than zero .', 'error_code': '6400'},
                                status=status.HTTP_400_BAD_REQUEST)

            price_new = Price(cpu=check_name[0].cpu, mem=check_name[0].mem, disk=check_name[0].disk, price=price,
                              host_model=host_model,
                              effective_date=effective_date, is_existed=is_existed)
            price_new.save()
            record_new = PriceAddRecord(price_uuid=price_new.price_uuid,
                                        action='add a new price,price=' + str(price) + ',host_model:' + host_model)
            record_new.save()
            return Response({'sattus': 'add price success'})
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            log.error('[price] veiws.create_price.e:{}'.format(e.__str__()))
            return Response({'detail': 'other error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='superadmin')
    def update(self, request, pk=None):
        """
        后台修改定价
        :param request:
        :return:
        """
        queryset = Price.objects.all()
        try:
            price = request.data.get('price')
            is_existed = request.data['is_existed']
            if request.data['price'] <= 0:
                return Response({'detail': 'price value is error'}, status=status.HTTP_400_BAD_REQUEST)
            price_obj = get_object_or_404(queryset, pk=pk)

            effective_date = request.data.get('effective_date')
            effective_date = datetime.datetime.strptime(effective_date, "%Y-%m-%dT%H:%M:%S.%fZ")
            effective_date = (effective_date + datetime.timedelta(hours=8)).date().replace(day=1)
            today = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).date()

            check_price = Price.objects.filter(is_existed=True,host_model=price_obj.host_model ,cpu=price_obj.cpu, mem=price_obj.mem, disk=price_obj.disk,
                                             effective_date__lte=today).order_by('-effective_date')
            if check_price.count()>0 and str(check_price[0].price_uuid)==pk:
                return Response({'detail': '不能修改已经生效的价格', 'error_code': '6400'},
                                status=status.HTTP_400_BAD_REQUEST)

            # check_name = Price.objects.filter(host_model=request.data['host_model'], is_existed=True)
            #
            # if check_name.count() == 1 and is_existed is False:
            #     return Response({'detail': '该配置的host必须有一个有效价格', 'error_code': '6400'},
            #                     status=status.HTTP_400_BAD_REQUEST)
            old_price = price_obj.price
            price_obj.is_existed = request.data['is_existed']
            price_obj.price = request.data['price']
            price_obj.effective_date = effective_date
            price_obj.host_model = request.data['host_model']
            price_obj.save()
            record_new = PriceAddRecord(price_uuid=pk, action='update a  price,from ' + str(old_price) + ' to ' + str(
                request.data['price']))
            record_new.save()
            return Response({'sattus': 'change price success'})
        except Price.DoesNotExist:
            return Response({'detail': 'the price startegy is not existed',
                             'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except TypeError:
            return Response({'detail': 'type error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[price] veiws.update. e:{}'.format(e.__str__()))
            return Response({'detail': 'other error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='user')
    def list(self, request):
        """
        提供给用户
        获取所有定价列表
        传入参数:
            url中携带参数：page(页数,默认为1），num(每页条目数，默认为10)
        """
        try:
            page = request.GET.get('page', 1)
            num = request.GET.get('num', 10)
            list1 = set(Price.objects.values_list('cpu', 'mem', 'disk'))
            prices_all = []
            for one in list1:
                tz = pytz.timezone('Asia/Shanghai')
                current_date = datetime.datetime.now(tz).date()
                price_obj = Price.objects.filter(is_existed=True, cpu=one[0], mem=one[1], disk=one[2],
                                                 effective_date__lte=current_date).order_by('-effective_date')
                if price_obj.count() != 0:
                    prices_all.append(price_obj[0])
            prices_all = prices_all[(int(page) - 1) * int(num):int(page) * int(num)]
            serializer = PriceSerializer(prices_all, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'detail': 'type error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[price] veiws.list. e:{}'.format(e.__str__()))
            return Response({'detail': 'other error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='user')
    @list_route(methods=['get'])
    def get_all_price(self, request):
        """
        提供给后台调用的接口
        :param request:
        :return:
        """
        try:
            prices_all = Price.objects.all().order_by('price')
            serializer = PriceSerializer(prices_all, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'detail': 'type error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[price] veiws.get_all_price. e:{}'.format(e.__str__()))
            return Response({'detail': 'other  error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)

    @auth_required(role='user')
    @list_route(methods=['get'])
    def get_price_bycondition(self, request):
        """
        根据条件获取相应的定价
        """
        try:
            cpu = request.data.get('cpu', None)
            mem = request.data.get('mem', None)
            disk = request.data.get('disk', None)
            price = Price.objects.filter(cpu=cpu).filter(disk=disk).filter(mem=mem)
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'badly formed hexadecimal UUID string', 'error_code': '6400'},
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'detail': 'other error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        if price.count() > 0:
            serializer = PriceSerializer(price[0])
            return Response(serializer.data)
        else:
            return Response({'detail': 'not found the price which meet the condition', 'error_code': '6400'},
                            status=status.HTTP_404_NOT_FOUND)


class RecordPriceViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    """
    queryset = PriceAddRecord.objects.all()
    serializer_class = RecordPriceSerializer

    def list(self, request):
        """
        获取一个定价策略的所有变更记录
        :param request:
        :return:
        """
        try:
            page = request.GET.get('page', 1)
            num = request.GET.get('num', 10)
            price_uuid = request.GET.get('price_uuid', None)
            if price_uuid is None:
                serializer_record = PriceAddRecord.objects.all()[
                                    (int(page) - 1) * int(num):int(page) * int(num)]
            else:
                serializer_record = PriceAddRecord.objects.filter(price_uuid=price_uuid)[
                                    (int(page) - 1) * int(num):int(page) * int(num)]
            serializer = RecordPriceSerializer(serializer_record, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response({'detail': 'type error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'detail': 'key error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error('[price] Record veiws.list. e:{}'.format(e.__str__()))
            return Response({'detail': 'other  error', 'error_code': '6400'}, status=status.HTTP_400_BAD_REQUEST)
