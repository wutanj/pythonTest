import unittest
import paramunittest
import readConfig as readConfig
from common import Log as Log
from common import units
from common import configHttp as ConfigHttp

configList_xls = units.get_xls('configData.xlsx', 'list')
localReadConfig = readConfig.ReadConfig()
localConfigHttp = ConfigHttp.ConfigHttp()
info = {}


@paramunittest.parametrized(*configList_xls)
class SdataList(unittest.TestCase):
    def setParameters(self, case_name, method, nameX, pageNumber, pageSize, result, code, data):
        """
        set params
        :param case_name:
        :param method:
        :param nameX:
        :param pageNumber:
        :param pageSize:
        :param result:
        :param code:
        :param data:
        :return:
        """
        self.case_name = str(case_name)
        self.method = str(method)
        self.nameX = str(nameX)
        self.pageNumber = int(pageNumber)
        self.pageSize = int(pageSize)
        self.result = int(result)
        self.code = int(code)
        self.data = str(data)
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

    def testSdataList(self):
        """
        test body
        :return:
        """
        # set url
        self.url = units.get_url_from_xml('sdataList')
        localConfigHttp.set_url(self.url)
        print("第一步： 设置url " + self.url)

        # get app_key
        # if self.app_key == '0':
        #     app_key = localReadConfig.get_headers("app_key")
        # elif self.app_key == '1':
        #     app_key = None

        # header = { 'Content-Type': "application/x-www-form-urlencoded"}
        # localConfigHttp.set_headers(header)

        # set params
        params = {
            "nameX": self.nameX,
            "pageNumber": self.pageNumber,
            "pageSize": self.pageSize,
        }
        localConfigHttp.set_params(params)
        print("第二步： 设置发送请求的参数" + str(params))
        print("第二步： 设置发送请求的参数" + str(params))

        # test interface
        self.return_json = localConfigHttp.get()
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
        data = units.get_value_from_return_json(self.info, "data")

        if self.result == 0:
            self.assertEqual(int(code), self.code)
            self.assertEqual(data, self.data)

        if self.result == 1:
            content = units.get_value_from_return_json(data, 'content')
            number = len(content)
            self.assertEqual(int(code), self.code)
            self.assertEqual(data, self.data)
            self.assertEqual(number, self.pageSize)
