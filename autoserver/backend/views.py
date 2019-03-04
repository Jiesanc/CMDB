import json
from django.shortcuts import render, HttpResponse
from repository import models

from datetime import datetime
from datetime import date
class JsonCustomEncoder(json.JSONEncoder):

    def default(self, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, value)

# Create your views here.

def get_data_list(request,model_cls,table_config):
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    from django.db.models import Q

    condition = request.GET.get('condition')
    condition_dict = json.loads(condition)

    con = Q()
    for name,values in condition_dict.items():
        ele = Q() # select xx from where cabinet_num=sdf or cabinet_num='123'
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name,item))
        con.add(ele, 'AND')

    server_list = model_cls.objects.filter(con).values(*values_list)
    return server_list


def curd(request):
    # v = models.Server.objects.all()
    return render(request, 'curd.html')


def curd_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        print(id_list)
        return HttpResponse('....')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        print(all_list)
        return HttpResponse('....')
    elif request.method == "POST":
        pass
    elif request.method == 'GET':
        from backend.page_config import curd as curdConfig
        server_list = get_data_list(request,models.Asset,curdConfig.table_config)
        ret = {
            'server_list': list(server_list),
            'table_config': curdConfig.table_config,
            'search_config':curdConfig.search_config,
             'global_dict':{
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices
            }
        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def asset(request):
    # v = models.Server.objects.all()
    return render(request, 'asset.html')


def asset_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        print(id_list)
        return HttpResponse('...')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        for row in all_list:
            nid = row.pop('id')
            models.Asset.objects.filter(id=nid).update(**row)
        return HttpResponse('....')
    elif request.method == "POST":
        pass
    elif request.method == 'GET':
        from backend.page_config import asset as assetConfig
        server_list = get_data_list(request,models.Asset,assetConfig.table_config)
        ret = {
            'server_list': list(server_list),
            'table_config': assetConfig.table_config,
            'global_dict':{
                'device_type_choices': models.Asset.device_type_choices,
                'device_status_choices': models.Asset.device_status_choices,
                'idc_choices': list(models.IDC.objects.values_list('id','name'))
            },
            'search_config':assetConfig.search_config

        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))


def idc(request):
    return render(request,'idc.html')

def idc_json(request):
    if request.method == 'DELETE':
        id_list = json.loads(str(request.body,encoding='utf-8'))
        print(id_list)
        return HttpResponse('。。。')
    elif request.method == "PUT":
        all_list = json.loads(str(request.body,encoding='utf-8'))
        print(all_list)
        return HttpResponse('。。。')
    elif request.method == 'GET':
        from backend.page_config import idc
        values_list = []
        for row in idc.table_config:
            if not row['q']:
                continue
            values_list.append(row['q'])

        server_list = models.IDC.objects.values(*values_list)

        ret = {
            'server_list': list(server_list),
            'table_config': idc.table_config,
            'global_dict':{}

        }
        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))