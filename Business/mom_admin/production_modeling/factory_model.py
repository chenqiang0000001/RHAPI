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
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureName": OrganizationStructureName,
            "OrganizationStructureDisplayName": "自动化专业车间（自动创建）",
            "OrganizationType": "WorkShopInfo",
            "OrganizationStructureExternalCode": "",
            "SortNum": 1,
            "Remark": "",
            "OpSign": 1,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreOrganizationStructureData = urlLogin1 + apiStoreOrganizationStructureData
        try:
            response = requests.post(url=urlStoreOrganizationStructureData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"正在执行：storeOrganizationStructureData，\nURL: {urlStoreOrganizationStructureData}，\n请求头: {self.headers}，\n请求体: {uploads},\n响应体为{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreOrganizationStructureData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def removeOrganizationStructureData(self,OrganizationStructureCode=OrganizationStructureCode, OrganizationStructureName=OrganizationStructureName):
        """
        删除车间
        :param OrganizationStructureCode: 车间编码
        :param OrganizationStructureName: 车间名称
        """
        uploads = {
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureParentCode": "00000.00001",
            "OrganizationStructureName": OrganizationStructureName,
            "OrganizationStructureDisplayName": OrganizationStructureName,
            "OrganizationGroup": "Product",
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
        }
        urlRemoveOrganizationStructureData = urlLogin1 + apiRemoveOrganizationStructureData
        try:
            response = requests.post(url=urlRemoveOrganizationStructureData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"正在执行：removeOrganizationStructureData，\nURL: {urlRemoveOrganizationStructureData}，\n请求头: {self.headers}，\n请求体: {uploads},\n响应体为{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveOrganizationStructureData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def storeOrganizationStructureData_productionline(self,OrganizationStructureParentCode=OrganizationStructureParentCode, OrganizationStructureCode2=OrganizationStructureCode2,OrganizationStructureName2=OrganizationStructureName2):
        """
        新增产线
        :param OrganizationStructureParentCode: 产线父节点编码
        :param OrganizationStructureCode2: 产线编码
        :param OrganizationStructureName2: 产线名称
        """
        # uploads = {
        #     "OrganizationStructureParentCode": OrganizationStructureParentCode,
        #     "OrganizationStructureCode": OrganizationStructureCode2,
        #     "OrganizationStructureName": OrganizationStructureName2,
        #     "ProductionLineType": "ProductLine",
        #     "OrganizationStructureDisplayName": "",
        #     "OrganizationStructureExternalCode": "",
        #     "OrganizationType": "ProductLine",
        #     "CompanyCode": "00000",
        #     "FactoryCode": "00000.00001"
        # }
        uploads = {
                "OrganizationStructureParentCode": OrganizationStructureParentCode,
                "OrganizationStructureCode": OrganizationStructureCode2,
                "OrganizationStructureName": OrganizationStructureName2,
                "ProductionLineType": "ProductLine",
                "OrganizationStructureDisplayName": "",
                "OrganizationStructureExternalCode": "",
                "SortNum": 1,
                "Remark": "",
                "OpSign": 1,
                "OrganizationType": "ProductLine",
                "CompanyCode": "00000",
                "FactoryCode": "00000.00001"
            }
        urlStoreOrganizationStructureData = urlLogin1 + apiStoreOrganizationStructureData
        try:
            response = requests.post(url=urlStoreOrganizationStructureData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"正在执行：storeOrganizationStructureData，\nURL: {urlStoreOrganizationStructureData}，\n请求头: {self.headers}，\n请求体: {uploads},\n响应体为{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreOrganizationStructureData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def removeOrganizationStructureData_productionline(self,OrganizationStructureParentCode=OrganizationStructureParentCode, OrganizationStructureCode2=OrganizationStructureCode2,OrganizationStructureName2=OrganizationStructureName2):
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
            "OrganizationStructureDisplayName": "",
            "OrganizationStructureExternalCode": "",
            "OrganizationType": "ProductLine",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
            }

        urlRemoveOrganizationStructureData = urlLogin1 + apiRemoveOrganizationStructureData
        try:
            response = requests.post(url=urlRemoveOrganizationStructureData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"正在执行：removeOrganizationStructureData，\nURL: {urlRemoveOrganizationStructureData}，\n请求头: {self.headers}，\n请求体: {uploads},\n响应体为{response.json()}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlRemoveOrganizationStructureData}，请求头: {self.headers}，请求体: {uploads}")
            raise e



if __name__ == '__main__':
    res1 = FactoryModel().storeOrganizationStructureData_productionline().json()
    # res2 = FactoryModel().removeOrganizationStructureData().json()
    print(res1)
    # print(res2)