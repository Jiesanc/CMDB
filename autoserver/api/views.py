import json
import hashlib
import time
from django.shortcuts import render,HttpResponse
from repository import models
from django.conf import settings
# redis/Memcache
api_key_record = {
    # "1b96b89695f52ec9de8292a5a7945e38|1501472467.4977243":1501472477.4977243
}

def decrypt(msg):
    from Crypto.Cipher import AES
    key = b'dfdsdfsasdfdsdfs'
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')

def asset(request):
    client_md5_time_key = request.META.get('HTTP_OPENKEY')
    client_md5_key,client_ctime =  client_md5_time_key.split('|')
    client_ctime = float(client_ctime)
    server_time = time.time()

    # 第一关
    if server_time-client_ctime > 10:
        return HttpResponse('【第一关】小伙子，别唬我，太长了')
    # 第二关
    temp = "%s|%s" %(settings.AUTH_KEY,client_ctime,)
    m = hashlib.md5()
    m.update(bytes(temp,encoding='utf-8'))
    server_md5_key = m.hexdigest()
    if server_md5_key != client_md5_key:
        return HttpResponse('【第二关】小子，你是不是修改时间了')

    for k in list(api_key_record.keys()):
        v = api_key_record[k]
        if server_time > v:
            del api_key_record[k]

    # 第三关:
    if client_md5_time_key in api_key_record:
        return HttpResponse('【第三关】有人已经来过了...')
    else:
        api_key_record[client_md5_time_key] = client_ctime + 10

    if server_md5_key != client_md5_key:
        return HttpResponse('认证失败...')
    if request.method == 'GET':
        ys = '重要的不能被闲杂人等看的数据'
        return HttpResponse(ys)

    elif request.method == 'POST':
        server_info = decrypt(request.body)
        server_info = json.loads(server_info)
        # 新资产信息
        hostname = server_info['basic']['data']['hostname']
        # 老资产信息
        server_obj = models.Server.objects.filter(hostname=hostname).first()
        if not server_obj:
            return HttpResponse('当前主机名在资产中未录入')

        for k,v in  server_info.items():
            print(k,v)

        # ############### 处理硬盘信息 ##################
        if not server_info['disk']['status']:
            models.ErrorLog.objects.create(content=server_info['disk']['data'],asset_obj=server_obj.asset,title='【%s】硬盘采集错误信息' %hostname)
        new_disk_dict = server_info['disk']['data']
        """
        {
            5: {'slot':5,capacity:476...}
            3: {'slot':3,capacity:476...}
        }
        """
        old_disk_list = models.Disk.objects.filter(server_obj=server_obj)
        """
        [
            Disk('slot':5,capacity:476...)
            Disk('slot':4,capacity:476...)
        ]
        """
        # 交集：5, 创建：3,删除4;
        new_slot_list = list(new_disk_dict.keys())

        old_slot_list = []
        for item in old_disk_list:
            old_slot_list.append(item.slot)

        # 交集：更新[5,]
        update_list = set(new_slot_list).intersection(old_slot_list)
        # 差集: 创建[3]
        create_list = set(new_slot_list).difference(old_slot_list)
        # 差集: 创建[4]
        del_list = set(old_slot_list).difference(new_slot_list)


        if del_list:
            # 删除
            models.Disk.objects.filter(server_obj=server_obj,slot__in=del_list).delete()
            # 记录日志
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content="移除硬盘：%s" %("、".join(del_list),) )

        # 增加、
        record_list = []
        for slot in create_list:
            disk_dict = new_disk_dict[slot] # {'capacity': '476.939', 'slot': '4', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series
            disk_dict['server_obj'] = server_obj
            models.Disk.objects.create(**disk_dict)
            temp = "新增硬盘:位置{slot},容量{capacity},型号:{model},类型:{pd_type}".format(**disk_dict)
            record_list.append(temp)
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)

        # ############ 更新 ############
        record_list = []
        row_map = {'capacity': '容量','pd_type': '类型','model':'型号'}
        for slot in update_list:
            new_dist_row = new_disk_dict[slot]
            ol_disk_row = models.Disk.objects.filter(slot=slot,server_obj=server_obj).first()
            for k,v in new_dist_row.items():
                # k: capacity;slot;pd_type;model
                # v: '476.939''xxies              DXM05B0Q''SATA'
                value = getattr(ol_disk_row,k)
                if v != value:
                    record_list.append("槽位%s,%s由%s变更为%s" %(slot,row_map[k],value,v,))
                    setattr(ol_disk_row,k,v)
            ol_disk_row.save()
        if record_list:
            content = ";".join(record_list)
            models.AssetRecord.objects.create(asset_obj=server_obj.asset,content=content)

















        # 资产表中以前资产信息
        # server_obj可以找到服务基本信息（单条）
        # disk_list = server_obj.disk.all()


        # 处理：
        """
        1. 根据新资产和原资产进行比较：新["5","1"]      老["4","5","6"]
        2. 增加: [1,]   更新：[5,]    删除：[4,6]
        3. 增加：
                server_info中根据[1,],找到资产详细：入库
           删除：
                数据库中找当前服务器的硬盘：[4,6]

           更新：[5,]
                disk_list = [obj,obj,obj]

                {
                    'data': {
                        '5': {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '3': {'slot': '3', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'},
                        '4': {'slot': '4', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'},
                        '0': {'slot': '0', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'},
                        '2': {'slot': '2', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'},
                        '1': {'slot': '1', 'capacity': '279.396', 'pd_type': 'SAS', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}
                    },

                    'status': True
                }

                log_list = []

                dict_info = {'slot': '5', 'capacity': '476.939', 'pd_type': 'SATA', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'},
                obj
                    if obj.capacity != dict_info['capacity']:
                        log_list.append('硬盘容量由%s变更为%s' %s(obj.capacity,dict_info['capacity'])
                        obj.capacity = dict_info['capacity']
                    ...
                obj.save()

                models.xxx.object.create(detail=''.join(log_list))

        """


            # 今天作业：(基本信息，硬盘，内存)

    return HttpResponse('...')
