import requests
from Public.address.mom import get_url, apiStoreProcessInfoData, apiRemoveProcessInfoData, apiGetProcessInfoAutoQueryDatas, apiStoreProcessRoutingData, apiRemoveProcessRoutingData, apiGetProcessRoutingAutoQueryDatas, apiGetProductProcessRouteAutoQueryDatas, apiRemoveBatchProductProcessRouteDatas, apiAdjustProcessRoutingEntry, apiStoreProductProcessRouteData, apiStoreBatchProductProcessRouteDatas, apiSelectManufactureBom
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.config_headers import get_headers

class ProcessRelated:
    """
    工序相关接口封装
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="ProcessRelated").get_logger()
        self.url = get_url()

    def storeProcessInfoData(self,ProcessCode=ProcessCode, ProcessName=ProcessName):
        """
        新增工序
        :param ProcessCode: 工序编码
        :param ProcessName: 工序名称
        :return:响应实例体对象
        """
        uploads = {
            "ProcessCode": ProcessCode,
            "ProcessName": ProcessName,
            "ProcessDescription": "",
            "EquipmentCode": None,
            "ProcessDisplayName": "",
            "IsReportCheck": False,
            "IsOutSide": False,
            "IsExportFlowCard": False,
            "IsUsePackingList": False,
            "IsPatrolInspect": False,
            "IsFirstInspect": True,
            "IsFinishInspect": False,
            "IsBindDispatchCode": False,
            "IsKeyComponent": False,
            "IsKittingCheck": False,
            "IsProcessAudit": False,
            "IsOutsourcing": False,
            "SupplierCode": None,
            "SupplierName": "",
            "Remark": "",
            "OpSign": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreProcessInfoData = self.url + apiStoreProcessInfoData
        try:
            response = requests.post(url=urlStoreProcessInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreProcessInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def GetProcessInfoAutoQueryDatas(self,ProcessCode=ProcessCode):
        """
        查询工序
        :param ProcessCode: 工序编码
        """
        uploads = {
            "ProcessCode": ProcessCode,
            "ProcessName": "",
            "PageSize": 10,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetProcessInfoAutoQueryDatas = self.url + apiGetProcessInfoAutoQueryDatas
        try:
            response = requests.post(url=urlGetProcessInfoAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetProcessInfoAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeProcessInfoData(self,processId):
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
            "Id": processId
        }
        urlRemoveProcessInfoData = self.url + apiRemoveProcessInfoData
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
        urlStoreProcessRoutingData = self.url + apiStoreProcessRoutingData
        try:
            response = requests.post(url=urlStoreProcessRoutingData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreProcessRoutingData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def getProcessRoutingAutoQueryDatas(self,ProcessRoutingCode=ProcessRoutingCode):
        """
        查询工艺路线
        :param ProcessRoutingCode: 工艺路线编码
        :return:响应实例体对象
        """
        uploads = {
            "ProcessRoutingCode": ProcessRoutingCode,
            "IsPaged": True,
            "PageSize": 10,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetProcessRoutingAutoQueryDatas = self.url + apiGetProcessRoutingAutoQueryDatas
        try:
            response = requests.post(url=urlGetProcessRoutingAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetProcessRoutingAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeProcessRoutingData(self,routing_id, ProcessRoutingName=ProcessRoutingName,ProcessRoutingCode=ProcessRoutingCode2):
        """
        删除工艺路线
        :param ProcessRoutingName: 工艺路线名称
        :param ProcessRoutingCode: 工艺路线编码
        :return:响应实例体对象
        """
        uploads = {
            "ProcessRoutingCode": ProcessRoutingCode,
            "ProcessRoutingName": ProcessRoutingName,
            "Id": routing_id,
            "ProcessRoutingBasisCode": "Automation01",
            "CreatorUserId": 150,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",

        }
        urlRemoveProcessRoutingData = self.url + apiRemoveProcessRoutingData
        try:
            response = requests.post(url=urlRemoveProcessRoutingData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveProcessRoutingData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def GetProductProcessRouteAutoQueryDatas(self,ProductCode=MaterialCode):
        """
        查询产品工艺路线
        :param MaterialCode: 物料编码
        :return:响应实例体对象
        """
        uploads = {
            "ProductCode": ProductCode,
            "IsPaged": True,
            "PageSize": 10,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetProductProcessRouteAutoQueryDatas = self.url + apiGetProductProcessRouteAutoQueryDatas
        try:
            response = requests.post(url=urlGetProductProcessRouteAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetProductProcessRouteAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def RemoveBatchProductProcessRouteDatas(self,product_process_id):
        """
        删除产品工艺路线
        :return:响应实例体对象
        """
        uploads = [{
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProcessRoutingCode": ProcessRoutingCode2,
            "ProcessRoutingName": ProcessRoutingName,
            "CreatorUserId": 150,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "Id": product_process_id
        }]
        urlRemoveBatchProductProcessRouteDatas = self.url + apiRemoveBatchProductProcessRouteDatas
        try:
            response = requests.post(url=urlRemoveBatchProductProcessRouteDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveBatchProductProcessRouteDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def adjustProcessRoutingEntry(self,ProcessRoutingCode=ProcessRoutingCode2,ProcessCode=ProcessCode,ProcessName=ProcessName):
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
        urlAdjustProcessRoutingEntry = self.url + apiAdjustProcessRoutingEntry
        try:
            response = requests.post(url=urlAdjustProcessRoutingEntry, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlAdjustProcessRoutingEntry}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def StoreProductProcessRouteData(self):
        """
        工艺路线绑定产品
        :param MaterialCode: 物料编码
        :param ProcessRoutingCode: 工艺路线编码
        :param ProcessRoutingName: 工艺路线名称
        :param MaterialName: 物料名称
        """
        uploads = {
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProcessRoutingCode": ProcessRoutingCode2,
            "ProcessRoutingName": ProcessRoutingName,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreProductProcessRouteData = self.url + apiStoreProductProcessRouteData
        try:
            response = requests.post(url=urlStoreProductProcessRouteData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreProductProcessRouteData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def StoreBatchProductProcessRouteDatas(self):
        """
        产品绑定工艺路线
        """
        uploads = [{
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "ProcessRoutingCode": ProcessRoutingCode2,
            "ProcessRoutingName": ProcessRoutingName,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }]
        urlStoreBatchProductProcessRouteDatas = self.url + apiStoreBatchProductProcessRouteDatas
        try:
            response = requests.post(url=urlStoreBatchProductProcessRouteDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreBatchProductProcessRouteDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def SelectManufactureBom(self,BOMVersion):
        """
        产品工序BOM绑定 接口
        """
        BOMBasicCode = BOMCode + '_' + BOMVersion
        uploads = {
            "BOMCode": BOMCode,
            "BOMBasicCode": BOMBasicCode,
            "FactoryCode": "00000.00001",
            "CompanyCode": "00000",
            "ProcessRoutingCode": ProcessRoutingCode2,
            "ProcessRoutingEntryCode": "1e56b589-ac1a-49ec-8e01-810847408e6d",
            "ProductCode": MaterialCode
        }
        urlSelectManufactureBom = self.url + apiSelectManufactureBom
        try:
            response = requests.post(url=urlSelectManufactureBom, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlSelectManufactureBom}，请求头: {self.headers}，请求体: {uploads}")
            return None

if __name__ == '__main__':
    res1 = ProcessRelated().SelectManufactureBom("WUPC8046757").json()
    # res2 = ProcessRelated().SelectManufactureBom().json()
    print(f"{res1}")
    # print(f"新增工序响应体为：{res2}")