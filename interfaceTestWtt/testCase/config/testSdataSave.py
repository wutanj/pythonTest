import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import units
from common import configHttp as ConfigHttp

configSave_xls = units.get_xls('configData.xlsx', 'save')
localReadConfig = readConfig.ReadConfig()
localConfigHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*configSave_xls)
class SdataSave(unittest.TestCase):
    def setParameters(self, case_name, method, configId, nameX, nameY, nameZ, value1, value2, result, code, msg):
        """
        set params
        :param case_name:
        :param method:
        :param configId:
        :param nameX:
        :param nameY:
        :param nameZ:
        :param value1:
        :param value2:
        :param result:
        :param code:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.configId = int(configId)
        self.nameX = str(nameX)
        self.nameY = str(nameY)
        self.nameZ = str(nameZ)
        self.value1 = str(value1)
        self.value2 = str(value2)
        self.result = int(result)
        self.code = int(code)
        self.msg = str(msg)
        self.return_json = None
        self.info = []

    def description(self):
        """
        test report description
        :return:
        """
        self.case_name

    def setUp(self):
        """

        :return:
        """
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        print(self.case_name + '测试开始前的准备')

    def testSdataSave(self):
        """
        test body
        :return:
        """
        # set url
        self.url = units.get_url_from_xml('sdataSave')
        localConfigHttp.set_url(self.url)
        print("第一步： 设置url " + self.url)

        # get app_key
        # if self.app_key == '0':
        #     app_key = localReadConfig.get_headers("app_key")
        # elif self.app_key == '1':
        #     app_key = None

        header = {'Content-Type': "application/x-www-form-urlencoded"}
        localConfigHttp.set_headers(header)

        # set params
        data = 'configId='+self.configId + '&nameX='+self.nameX+'&nameY='+self.nameY+'&nameZ='+self.nameZ+'&value1='+self.value1+'&value2='+self.value2
        #     {
        #     "nameX": self.nameX,
        #     "nameY": self.nameY,
        #     "nameZ": self.nameZ,
        #     "value1": self.value1,
        #     "value2": self.value2
        # }
        localConfigHttp.set_data(data)
        print("第二步： 设置发送请求的参数" + data)

        # test interface
        self.return_json = localConfigHttp.post()
        method = str(self.return_json.request)[
                 int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        print("第三步： 发送请求\n\t\t请求方法：" + method)

        # check result
        self.checkResult()
        print("第四步： 检查结果")

    def tearDown(self):
        """

        :return:
        """
        info = self.info
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """
        check test result
        :return:
        """
        self.info = self.return_json.json()
        # show return message
        units.show_return_msg(self.return_json)

        code = units.get_value_from_return_json(self.info, "code")
        msg = units.get_value_from_return_json(self.info, "message")

        if self.result == 0:
            self.assertEqual(int(code), self.code)
            self.assertEqual(msg, self.msg)

        if self.result == 1:
            self.assertEqual(int(code), self.code)
            self.assertEqual(msg, self.msg)
