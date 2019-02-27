import os
from lib.conf.config import settings


# 往当前环境变量的默认字典中加入配置文件的路径
os.environ['USER_SETTINGS'] = "config.settings"

