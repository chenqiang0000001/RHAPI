import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class FactoryModel:
    """
    工厂建模相关接口
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="FactoryModel").get_logger()

    def storeOrganizationStructureData(self,OrganizationStructureCode=OrganizationStructureCode, OrganizationStructureName=OrganizationStructureName):
        """
        新增车间
        :param OrganizationStructureCode: 车间编码
        :param OrganizationStructureName: 车间名称
        """
        uploads = {
            "OrganizationStructureParentCode": "00000.00001",
            "WorkShopInfoCode": OrganizationStructureCode,
            "WorkShopInfoName": OrganizationStructureName,
            "OrganizationType": "WorkShopInfo",
            "WorkShopInfoDescription": "",
            "OrganizationStructureExternalCode": "",
            "SortNum": 1,
            "IsEnable": True,
            "Remark": "",
            "OpSign": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreWorkShopInfoData = testUrl + apiStoreWorkShopInfoData
        try:
            response = requests.post(url=urlStoreWorkShopInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreWorkShopInfoData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def GetWorkshopAutoQueryDatas(self):
        """
        查询车间  目前只适用于编码配置为手动生成，后期判断下配置是否为手动生成
        :param OrganizationStructureCode: 车间编码
        :param OrganizationStructureName: 车间名称
        """
        uploads = {
            "WorkShopInfoCode": OrganizationStructureCode,
            "IsEnable": True,
            "WorkShopInfoName": OrganizationStructureName,
            "IsPaged": True,
            "PageSize": 40,
            "PageIndex": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetAllWorkShopInfoAutoQueryDatas = testUrl + apiGetAllWorkShopInfoAutoQueryDatas
        try:
            response = requests.post(url=urlGetAllWorkShopInfoAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetAllWorkShopInfoAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def removeOrganizationStructureData(self,workshop_id,OrganizationStructureCode=OrganizationStructureCode, OrganizationStructureName=OrganizationStructureName):
        """
        删除车间
        :param OrganizationStructureCode: 车间编码
        :param OrganizationStructureName: 车间名称
        """
        uploads = {
            "WorkShopInfoCode": OrganizationStructureCode,
            "WorkShopInfoName": OrganizationStructureName,
            "WorkShopInfoType": "WorkShopInfo",
            "OrganizationStructureParentCode": "00000.00001",
            "IsEnable": False,
            "SortNum": 1,
            "IsV2": False,
            "CreatorUserId": 150,
            "CreatorUserName": "DemoAdmin",
            "CreatorUserRealName": "DemoAdmin",
            "CreationTime": "2025-06-27T13:12:28.147+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": workshop_id,
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": False,
            "__edit": True,
            "__edit_disable": False,
            "__delete": True,
            "__delete_disable": False,
            "__parameterConfig": True,
            "__parameterConfig_disable": False
        }
        urlRemoveWorkShopInfoData = testUrl + apiRemoveWorkShopInfoData
        try:
            response = requests.post(url=urlRemoveWorkShopInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveWorkShopInfoData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def storeOrganizationStructureData_productionline(self,OrganizationStructureParentCode=OrganizationStructureCode, OrganizationStructureCode2=OrganizationStructureCode2,OrganizationStructureName2=OrganizationStructureName2):
        """
        新增产线
        :param OrganizationStructureParentCode: 产线父节点编码
        :param OrganizationStructureCode2: 产线编码
        :param OrganizationStructureName2: 产线名称
        """
        uploads = {
            "OrganizationStructureParentCode": OrganizationStructureParentCode,
            "ProductionLineCode": OrganizationStructureCode2,
            "ProductionLineName": OrganizationStructureName2,
            "ProductionLineType": "ProductLine",
            "ProductionLineDescription": "",
            "OrganizationStructureExternalCode": "",
            "SortNum": 1,
            "IsEnable": True,
            "Remark": "",
            "OpSign": 1,
            "OrganizationType": "ProductLine",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreProductionLineData = testUrl + apiStoreProductionLineData
        try:
            response = requests.post(url=urlStoreProductionLineData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreProductionLineData}，请求头: {self.headers}，请求体: {uploads}")
            raise e


    def GetProductionLineAutoQueryDatas(self,OrganizationStructureCode=OrganizationStructureCode2):
        """
        查询产线
        :param OrganizationStructureCode: 产线编码
        """
        uploads = {
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureName": "",
            "PageSize": 10,
            "PageIndex": 1,
           }
        urlGetAllProductionLineAutoQueryDatas = testUrl + apiGetAllProductionLineAutoQueryDatas
        try:
            response = requests.post(url=urlGetAllProductionLineAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetAllProductionLineAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def removeOrganizationStructureData_productionline(self,productionline_id,OrganizationStructureParentCode=OrganizationStructureCode, OrganizationStructureCode2=OrganizationStructureCode2,OrganizationStructureName2=OrganizationStructureName2):
        """
        删除产线
        :param OrganizationStructureCode: 产线编码
        :param OrganizationStructureName: 产线名称
        """
        uploads = {
            "OrganizationStructureParentCode": OrganizationStructureParentCode,
            "OrganizationStructureCode": OrganizationStructureCode2,
            "OrganizationStructureName": OrganizationStructureName2,
            "ProductionLineType": "ProductLine",
            "OrganizationType": "ProductLine",
            "Id": productionline_id,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
            }

        urlRemoveProductionLineData = testUrl + apiRemoveProductionLineData
        try:
            response = requests.post(url=urlRemoveProductionLineData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveProductionLineData}，请求头: {self.headers}，请求体: {uploads}")
            raise e



if __name__ == '__main__':
    factory_model = FactoryModel()
    res1 = factory_model.storeOrganizationStructureData().json()  # 新增车间
    res2 = factory_model.GetWorkshopAutoQueryDatas().json() # 查询车间
    id = res2['Attach'][0]['Id']

    # res3 = factory_model.removeOrganizationStructureData(id).json() # 删除车间
    res3 = factory_model.storeOrganizationStructureData_productionline().json() # 新增产线
    res4 = factory_model.GetProductionLineAutoQueryDatas().json()  # 查询产线
    print(f" res1 = {res1}, res2 = {res2}, res3 = {res3}")
    print(res1)