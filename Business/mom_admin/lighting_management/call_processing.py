import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class AndenCallProcessing:
    """
    安灯呼叫与处理
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="AndenCallProcessing").get_logger()

    def StoreAndonCallDataRecordsData(self,ProductionPlanCode):
        """
        安灯呼叫
        :param ProductionPlanCode: 生产计划单编码
        :return: 响应对象
        """
        uploads = {
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProductSpecification": "",
            "ProductionPlanCode": ProductionPlanCode,
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "CallProblemCode": "ZHD-LB",
            "CallProblemName": "自动化测试产生原因一级分类",
            "CallTwoProblemCode": "ZDH02",
            "CallTwoProblemName": "自动化测试产生原因二级分类",
            "CallerCode": "CQ",
            "CallerName": "CQ",
            "CallLocationCode": EquipmentCode,
            "CallLocationName": EquipmentName,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreAndonCallDataRecordsData = url + apiStoreAndonCallDataRecordsData
        try:
            response = requests.post(url=urlStoreAndonCallDataRecordsData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"安灯呼叫响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreAndonCallDataRecordsData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def ResponseAndonCallDataRecordsData(self,OrderCode, call_out_id):
        """
        安灯签到
        :param OrderCode: 安灯呼叫编码
        :param call_out_id: 安灯呼叫ID
        :return: 响应对象
        """
        uploads = {
            "OrderCode": OrderCode,
            "OrderStatus": "Call",
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProductSpecification": "",
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "CallProblemCode": "ZHD-LB",
            "CallProblemName": "自动化测试产生原因一级分类",
            "CallTwoProblemCode": "ZDH02",
            "CallTwoProblemName": "自动化测试产生原因二级分类",
            "CallLocationCode": EquipmentCode,
            "CallLocationName": EquipmentName,
            "CallIp": "192.168.82.204",
            "CallDate": "2025-07-10T17:01:23.91+08:00",
            "CallMonth": 7,
            "CallYear": 2025,
            "CallRuleGrade": 1,
            "CallTime": "2025-07-10T17:01:23.91+08:00",
            "CallerCode": "CQ",
            "CallerName": "CQ",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "EndProcessorCode": "CQ",
            "EndProcessorName": "CQ",
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-07-10T17:01:23.97+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {
                "Id": call_out_id,
                "ResponseTime": "2025-07-10T09:02:48.439Z"
            },
            "Id": call_out_id,
        }
        urlResponseAndonCallDataRecordsData = url + apiResponseAndonCallDataRecordsData
        try:
            response = requests.post(url=urlResponseAndonCallDataRecordsData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"安灯签到响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlResponseAndonCallDataRecordsData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def StartProcessAndonCallDataRecordsData(self, OrderCode, call_out_id):
        """
        安灯开始处理
        :param OrderCode: 安灯呼叫编码
        :param call_out_id: 安灯呼叫ID
        :return: 响应对象
        """
        uploads = {
            "OrderCode": OrderCode,
            "OrderStatus": "Response",
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProductSpecification": "",
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "CallProblemCode": "ZHD-LB",
            "CallProblemName": "自动化测试产生原因一级分类",
            "CallTwoProblemCode": "ZDH02",
            "CallTwoProblemName": "自动化测试产生原因二级分类",
            "CallLocationCode": EquipmentCode,
            "CallLocationName": EquipmentName,
            "CallIp": "192.168.82.204",
            "CallDate": "2025-07-10T17:01:23.91+08:00",
            "CallMonth": 7,
            "CallYear": 2025,
            "CallRuleGrade": 1,
            "CallTime": "2025-07-10T17:01:23.91+08:00",
            "CallerCode": "CQ",
            "CallerName": "CQ",
            "ResponseTime": "2025-07-10T17:02:48.44+08:00",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "StartProcessTime": "2025-07-10T09:22:32.833Z",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "EndProcessorCode": "CQ",
            "EndProcessorName": "CQ",
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-07-10T17:01:23.97+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-07-10T17:02:48.48+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {
                "Id": call_out_id,
                "StartProcessTime": "2025-07-10T09:22:32.833Z"
            },
            "Id": call_out_id,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__startProcess": True,
            "__startProcess_disable": False,
            "__endProcess": False,
            "OpSign": 2
        }
        urlStartProcessAndonCallDataRecordsData = url + apiStartProcessAndonCallDataRecordsData
        try:
            response = requests.post(url=urlStartProcessAndonCallDataRecordsData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"安灯开始处理响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStartProcessAndonCallDataRecordsData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def EndProcessAndonCallDataRecordsData(self, OrderCode, call_out_id):
        """
        安灯结束处理
        :param OrderCode: 安灯呼叫编码
        :param call_out_id: 安灯呼叫ID
        :return: 响应对象
        """
        uploads = {
            "OrderCode": OrderCode,
            "OrderStatus": "StartProcess",
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProductSpecification": "",
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "CallProblemCode": "ZHD-LB",
            "CallProblemName": "自动化测试产生原因一级分类",
            "CallTwoProblemCode": "ZDH02",
            "CallTwoProblemName": "自动化测试产生原因二级分类",
            "ConfirmCallProblemCode": "ZHD-LB",
            "ConfirmCallProblemName": "自动化测试产生原因一级分类",
            "ConfirmCallTwoProblemCode": "ZDH02",
            "ConfirmCallTwoProblemName": "自动化测试产生原因二级分类",
            "CallLocationCode": EquipmentCode,
            "CallLocationName": EquipmentName,
            "CallIp": "192.168.82.204",
            "CallDate": "2025-07-10T17:01:23.91+08:00",
            "CallMonth": 7,
            "CallYear": 2025,
            "CallRuleGrade": 1,
            "CallTime": "2025-07-10 17:28:49",
            "CallerCode": "CQ",
            "CallerName": "CQ",
            "ResponseTime": "2025-07-10T17:02:48.44+08:00",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "StartProcessTime": "2025-07-10T17:22:32.833+08:00",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "EndProcessorCode": "",
            "EndProcessorName": "CQ",
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "ProcessResult": "通过",
            "ProcessDescription": "",
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-07-10T17:01:23.97+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-07-10T17:22:39.65+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {
                "Id": call_out_id,
                "EndProcessTime": "2025-07-10T09:28:49.169Z",
                "ConfirmCallProblemCode": "ZHD-LB",
                "ConfirmCallProblemName": "自动化测试产生原因一级分类",
                "ConfirmCallTwoProblemCode": "ZDH02",
                "ConfirmCallTwoProblemName": "自动化测试产生原因二级分类",
                "ProcessResult": "通过",
                "ProcessDescription": ""
            },
            "Id": call_out_id,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__startProcess": False,
            "__endProcess": True,
            "__endProcess_disable": False,
            "OpSign": 2
        }
        urlEndProcessAndonCallDataRecordsData = url + apiEndProcessAndonCallDataRecordsData
        try:
            response = requests.post(url=urlEndProcessAndonCallDataRecordsData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"安灯结束处理响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlEndProcessAndonCallDataRecordsData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def ConfirmAndonCallDataRecordsData(self, OrderCode, call_out_id):
        """
        安灯结束确认
        :param OrderCode: 安灯呼叫编码
        :param call_out_id: 安灯呼叫ID
        :return: 响应对象
        """
        uploads = {
            "OrderCode": OrderCode,
            "OrderStatus": "EndProcess",
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "CallCategoryCode": "ZDH",
            "CallCategoryName": "自动化测试一级分类",
            "CallCategoryItemCode": "ZDH02",
            "CallCategoryItemName": "自动化测试二级分类",
            "CallProblemCode": "ZHD-LB",
            "CallProblemName": "自动化测试产生原因一级分类",
            "CallTwoProblemCode": "ZDH02",
            "CallTwoProblemName": "自动化测试产生原因二级分类",
            "ConfirmCallProblemCode": "ZHD-LB",
            "ConfirmCallProblemName": "自动化测试产生原因一级分类",
            "ConfirmCallTwoProblemCode": "ZDH02",
            "ConfirmCallTwoProblemName": "自动化测试产生原因二级分类",
            "CallLocationCode": EquipmentCode,
            "CallLocationName": EquipmentName,
            "CallIp": "192.168.82.204",
            "CallDate": "2025-07-10T17:01:23.91+08:00",
            "CallMonth": 7,
            "CallYear": 2025,
            "CallRuleGrade": 1,
            "CallTime": "2025-07-10T17:01:23.91+08:00",
            "CallerCode": "CQ",
            "CallerName": "CQ",
            "ResponseTime": "2025-07-10T17:02:48.44+08:00",
            "ResponsePersonCode": "CQ",
            "ResponsePersonName": "CQ",
            "StartProcessTime": "2025-07-10T17:22:32.833+08:00",
            "StartProcessorCode": "CQ",
            "StartProcessorName": "CQ",
            "EndProcessTime": "2025-07-10T17:28:49.17+08:00",
            "EndProcessorCode": "CQ",
            "EndProcessorName": "CQ",
            "TotalProcessTime": 0.1045,
            "CheckerCode": "CQ",
            "CheckerName": "CQ",
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-07-10T17:01:23.97+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-07-10T17:28:49.157+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {
                "CheckTime": "2025-07-10 17:35:55",
                "Id": call_out_id
            },
            "Id": call_out_id,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__confirm": True,
            "__confirm_disable": False
        }
        urlConfirmAndonCallDataRecordsData = url + apiConfirmAndonCallDataRecordsData
        try:
            response = requests.post(url=urlConfirmAndonCallDataRecordsData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"安灯结束确认响应{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlConfirmAndonCallDataRecordsData}，请求头: {self.headers}，请求体: {uploads}")
            raise e


if __name__ == '__main__':
    res = AndenCallProcessing().StoreAndonCallDataRecordsData("PL202504180343")
    print(res.json())
