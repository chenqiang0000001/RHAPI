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

    def removeBatchEquipmentLedger(self,EquipmentCode=EquipmentCode, EquipmentName=EquipmentName):
        """
        删除设备台账
        :param EquipmentCode: 设备编码
        :param EquipmentName: 设备名称
        """
        uploads = [{
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
        }]
        urlRemoveBatchEquipmentLedger = url + apiRemoveBatchEquipmentLedger
        try:
            response = requests.post(url=urlRemoveBatchEquipmentLedger, headers=self.headers, json=uploads)
            
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveBatchEquipmentLedger}，请求头: {self.headers}，请求体: {uploads}")
            raise RuntimeError(f"设备台账删除失败: {str(e)}") from e

if __name__ == '__main__':
    res = EquipmentLedgerManagement().removeBatchEquipmentLedger().json()
    print(res)