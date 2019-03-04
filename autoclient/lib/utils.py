__author__ = 'Administrator'
from Crypto.Cipher import AES
from lib.conf.config import settings
def encrypt(message):
    """
    数据加密
    :param message:
    :return:
    """
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    ba_data = bytearray(message,encoding='utf-8')
    v1 = len(ba_data)
    v2 = v1 % 16
    if v2 == 0:
        v3 = 16
    else:
        v3 = 16 - v2
    for i in range(v3):
        ba_data.append(v3)
    final_data = ba_data.decode('utf-8')
    msg = cipher.encrypt(final_data) # 要加密的字符串，必须是16个字节或16个字节的倍数
    return msg

def decrypt(msg):
    """
    数据解密
    :param message:
    :return:
    """
    from Crypto.Cipher import AES
    key = settings.DATA_KEY
    cipher = AES.new(key, AES.MODE_CBC, key)
    result = cipher.decrypt(msg) # result = b'\xe8\xa6\x81\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0\xe5\xaf\x86\xe5\x8a\xa0sdfsd\t\t\t\t\t\t\t\t\t'
    data = result[0:-result[-1]]
    return str(data,encoding='utf-8')


def auth():
    """
    API验证
    :return:
    """
    import time
    import requests
    import hashlib

    ctime = time.time()
    key = "asdfasdfasdfasdf098712sdfs"
    new_key = "%s|%s" %(key,ctime,)

    m = hashlib.md5()
    m.update(bytes(new_key,encoding='utf-8'))  #里面是字节数据
    md5_key = m.hexdigest()                    #返回值是字符窜类型

    md5_time_key = "%s|%s" %(md5_key,ctime)

    return md5_time_key

