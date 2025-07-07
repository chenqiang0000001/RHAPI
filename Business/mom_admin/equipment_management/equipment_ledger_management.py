import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class EquipmentLedgerManagement:
    """
    设备台账管理接口封装
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="EquipmentLedgerManagement").get_logger()
    def storeEquipmentLedgerData(self,EquipmentCode=EquipmentCode, EquipmentName=EquipmentName):
        """
        新增设备台账
        :param EquipmentCode: 设备编码
        :param EquipmentName: 设备名称
        """
        uploads = {
            "EquipmentCode": EquipmentCode,
            "EquipmentName": EquipmentName,
            "OrganizationStructureCode": "00000.00001.00001",
            "StopTime": 3,
            "EquipmentGroupCode": "Q",
            "OrganizationStructureName": "注塑车间",
            "OrganizationStructureExternalCode": "ZSCJ",
            "EquipmentGroupName": "Q组",
            "OpSign": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreEquipmentLedgerData = url + apiStoreEquipmentLedgerData
        try:
            response = requests.post(url=urlStoreEquipmentLedgerData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreEquipmentLedgerData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def getEquipmentLedgerAutoQueryDatas(self,EquipmentCode=EquipmentCode, EquipmentName=EquipmentName):
        """
        查询设备台账
        :param EquipmentCode: 设备编码
        :param EquipmentName: 设备名称
        """
        uploads = {
            "EquipmentCode": EquipmentCode,
            "EquipmentName": EquipmentName,
            "PageSize": 10,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetEquipmentLedgerAutoQueryDatas = url + apiGetEquipmentLedgerAutoQueryDatas
        try:
            response = requests.post(url=urlGetEquipmentLedgerAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetEquipmentLedgerAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def removeBatchEquipmentLedger(self,equipment_id):
        """
        删除设备台账
        :param equipment_id: 设备ID
        """
        uploads = [{
            "EquipmentCode": EquipmentCode,
            "EquipmentName": EquipmentName,
            "EquipmentGroupCode": "Q",
            "EquipmentGroupName": "Q组",
            "OrganizationStructureCode": "00000.00001.00001",
            "OrganizationStructureName": "注塑车间",
            "OrganizationStructureExternalCode": "ZSCJ",
            "StopTime": 3,
            "CreatorUserId": 10418,
            "CreatorUserName": "zdh01",
            "CreatorUserRealName": "自动化测试专用账号（勿动）",
            "LastModifierUserRealName": "",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": equipment_id
        }]
        urlRemoveBatchEquipmentLedger = url + apiRemoveBatchEquipmentLedger
        try:
            response = requests.post(url=urlRemoveBatchEquipmentLedger, headers=self.headers, json=uploads)
            
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveBatchEquipmentLedger}，请求头: {self.headers}，请求体: {uploads}")
            raise RuntimeError(f"设备台账删除失败: {str(e)}") from e

if __name__ == '__main__':
    response3 = EquipmentLedgerManagement().storeEquipmentLedgerData().json()
    response = EquipmentLedgerManagement().getEquipmentLedgerAutoQueryDatas().json()
    Id = response['Attach'][0]['Id']
    response2 = EquipmentLedgerManagement().removeBatchEquipmentLedger(Id).json()
    print(Id)
    print(response2)
    print(response3)