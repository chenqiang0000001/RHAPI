import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class ProcessRelated:
    """
    工艺相关接口封装
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="ProcessRelated").get_logger()

    def storeProcessInfoData(self,ProcessCode=ProcessCode, ProcessName=ProcessName):
        """
        新增工序
        :param ProcessCode: 工序编码
        :param ProcessName: 工序名称
        :return:响应实例体对象
        """
        uploads = {
            "ProcessCode":ProcessCode,
            "ProcessName":ProcessName
        }
        urlStoreProcessInfoData = url + apiStoreProcessInfoData
        try:
            response = requests.post(url=urlStoreProcessInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            self.logger.info(f"当前执行新增工序接口：storeProcessInfoData，\n请求 URL: {urlStoreProcessInfoData}，\n请求头: {self.headers}，\n请求体: {uploads}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreProcessInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeProcessInfoData(self,ProcessCode=ProcessCode, ProcessName=ProcessName):
        """
        删除工序
        :param ProcessCode: 工序编码
        :param ProcessName: 工序名称
        :return:响应实例体对象
        """
        uploads = {
            "ProcessCode": ProcessCode,
            "ProcessName": ProcessName,
            "CompanyCode": CompanyCode,
        }
        urlRemoveProcessInfoData = url + apiRemoveProcessInfoData
        try:
            response = requests.post(url=urlRemoveProcessInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveProcessInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def storeProcessRoutingData(self,ProcessRoutingName=ProcessRoutingName,ProcessRoutingBasisCode=ProcessRoutingCode):
        """
        新建工艺路线
        :param ProcessRoutingName: 工艺路线名称
        :param ProcessRoutingBasisCode: 工艺路线编码
        :return:响应实例体对象
        """
        uploads = {
            "ProcessRoutingBasisCode": ProcessRoutingBasisCode,
            "ProcessRoutingName": ProcessRoutingName,
            "CompanyCode": CompanyCode,
        }
        urlStoreProcessRoutingData = url + apiStoreProcessRoutingData
        try:
            response = requests.post(url=urlStoreProcessRoutingData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreProcessRoutingData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeProcessRoutingData(self,ProcessRoutingName=ProcessRoutingName,ProcessRoutingCode=ProcessRoutingCode1):
        """
        删除工艺路线
        :param ProcessRoutingName: 工艺路线名称
        :param ProcessRoutingCode: 工艺路线编码
        :return:响应实例体对象
        """
        uploads = {
            "ProcessRoutingCode": ProcessRoutingCode,
            "ProcessRoutingName": ProcessRoutingName,
            "CompanyCode": CompanyCode,
        }
        urlRemoveProcessRoutingData = url + apiRemoveProcessRoutingData
        try:
            response = requests.post(url=urlRemoveProcessRoutingData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveProcessRoutingData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def adjustProcessRoutingEntry(self,ProcessRoutingCode=ProcessRoutingCode1,ProcessCode=ProcessCode,ProcessName=ProcessName):
        """
        工艺路线绑定工序
        :param ProcessCode: 工序编码
        :param ProcessName: 工序名称
        :param ProcessRoutingCode: 工艺路线编码
        :return: 响应实例体对象
        """
        uploads = {
                    "ProcessRoutingCode": ProcessRoutingCode,
                    "StoreList": [{
                        "ProcessCode": ProcessCode,
                        "ProcessName": ProcessName,
                    }],
                    "CompanyCode": CompanyCode, #公司代码
                }
        urlAdjustProcessRoutingEntry = url + apiAdjustProcessRoutingEntry
        # print(f"请求 URL: {urlAdjustProcessRoutingEntry},\n请求头: {self.headers}，\n请求体: {uploads}")
        try:
            response = requests.post(url=urlAdjustProcessRoutingEntry, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlAdjustProcessRoutingEntry}，请求头: {self.headers}，请求体: {uploads}")
            return None

if __name__ == '__main__':
    res = ProcessRelated().storeProcessInfoData().json()
    print(f"响应体为：{res}")
