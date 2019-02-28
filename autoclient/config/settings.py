"""
用户自定义配置文件
"""
import os

BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER = 'root'
PWD = "sdfsdf"

MODE = "AGENT" # SALT,SSH
# MODE = "SALT" # SALT,SSH

DEBUG = True


SSH_USER = "root"
SSH_PWD = "root"
SSH_KEY = "/xxx/xxx/xx"
SSH_PORT = 22



PLUGINS_DICT = {
    'basic': "src.plugins.basic.Basic",
    'board': "src.plugins.board.Board",
    'cpu': "src.plugins.cpu.Cpu",
    'disk': "src.plugins.disk.Disk",
    'memory': "src.plugins.memory.Memory",
    'nic': "src.plugins.nic.Nic",
}

# API = "http://www.oldboyedu.com"
API = "http://127.0.0.1:8000/api/asset.html"

CERT_PATH = os.path.join(BASEDIR,'config','cert')