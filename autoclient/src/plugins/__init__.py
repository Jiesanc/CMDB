from lib.conf.config import settings
import importlib

class PlugManager(object):

    def __init__(self, hostname=None):
        # 中控机中需要hostname
        self.hostname = hostname
        # 获得配置文件中的字典
        self.plugin_dict = settings.PLUGINS_DICT
        # 获得模式
        self.mode = settings.MODE

    def exec_plugin(self):
        """
        获取所有的插件并执行获取返回值


        通过配置文件一次性获得所有需要采集信息的类
        每个类中都实现统一个方法process()获取采集信息,并返回

        :return:
        """

        response = {}
        for k, v in self.plugin_dict.items:
            module_path, class_name = v.rsplit('.', 1)
            m = importlib.import_module(module_path)
            cls = getattr(m, class_name)
            result = cls().process(self.commond)
            response[k] = result

    def commond(self, cmd):
        if self.mode == "AGENT":
            return self.__agent



    def __agent(self, cmd):
        pass

    def __ssh(self, cmd):
        pass

    def __salt(self, cmd):
        pass





