import os
import importlib
from lib.conf import global_settings


class Settings(object):

    def __init__(self):

        # #### 默认的配置文件内容 ####
        for name in dir(global_settings):
            if name.isupper():
                value = getattr(global_settings, name)
                setattr(self, name, value)

        # ####  可更改的配置文件内容   ###
        settings_module = os.environ.get('USER_SETTINGS', None)
        if not settings_module:
            return
        # 相当于 from config import settings
        module = importlib.import_module(settings_module)
        for name in dir(module):
            if name.isupper():
                value = getattr(module, name)
                # 把得到的配置信息赋值给这个类,变成类的属性
                setattr(self, name, value)


settings = Settings()
