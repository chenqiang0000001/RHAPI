import requests
from Public.address.mom import get_url, apiStoreMaterialInfoData, apiGetMaterialInfoAutoQueryDatas, apiRemoveMaterialInfoData, apiGetBomMasterViewAutoQueryDatas, apiStoreManufactureBomData, apiStoreBatchManufactureBomDetailDatas, apiRemoveManufactureBomData
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.config_headers import get_headers


class ProductMaterials:
    """
    产品物料相关接口封装
    """

    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="ProductMaterials").get_logger()
        self.url = get_url()

    def storeMaterialInfoData(self, MaterialCode=MaterialCode, MaterialName=MaterialName):
        """
        新增产品物料
        :param MaterialCode: 物料编码
        :param MaterialName: 物料名称
        :param MaterialProperty: 物料特性
        :return: MaterialAttribute:物料属性
        :return: 响应实例体对象
        """
        uploads = uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "materialCharacteristic": [
                {
                    "label": "成品",
                    "value": "IsProduct",
                    "customData": {"checked": True},  # JSON true → Python True
                    "checked": True  # JSON true → Python True
                },
                {
                    "label": "半成品",
                    "value": "IsSemiFinishedProduct",
                    "customData": {"checked": True},
                    "checked": True
                },
                {
                    "label": "物料",
                    "value": "IsMaterial",
                    "customData": {"checked": True},
                    "checked": True
                }
            ],
            "MaterialCategoryCode": "DQJ",
            "MaterialAttribute": "SelfCreated",
            "MaterialSpecification": "",
            "MaterialDrawCode": None,  # JSON null → Python None
            "MaterialUnit": None,
            "MaterialAuxUnit": None,
            "MaterialVersion": "",
            "DataSource": "",
            "IsUse": True,  # JSON true → Python True
            "IsChecked": False,  # JSON false → Python False
            "Remark": "",
            "OpSign": 1,
            "MaintainerId": 10402,
            "MaintainerName": "CQ",
            "MaintainTime": "2025-06-25T06:07:33.626Z",
            "IsProduct": True,
            "IsSemiFinishedProduct": True,
            "IsMaterial": True,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreMaterialInfoData = self.url + apiStoreMaterialInfoData
        try:
            response = requests.post(url=urlStoreMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreMaterialInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def getMaterialInfoAutoQueryDatas(self,MaterialCode=MaterialCode):
        """
        物料查询接口
        :param MaterialCode: 物料代码
        :return: 响应实例体对象
        """
        uploads = {
            "MaterialCode":MaterialCode
        }
        urlGetMaterialInfoAutoQueryDatas = self.url + apiGetMaterialInfoAutoQueryDatas
        try:
            response = requests.post(url=urlGetMaterialInfoAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetMaterialInfoAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeMaterialInfoData(self,material_id, MaterialCode=MaterialCode,MaterialName=MaterialName):
        """
        删除物料
        :param MaterialCode: 物料编码
        :param MaterialName: 物料名称
        :return: 响应实例体对象
        """
        uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "Id": material_id
        }
        urlRemoveMaterialInfoData = self.url + apiRemoveMaterialInfoData
        try:
            response = requests.post(url=urlRemoveMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveMaterialInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

class MaterialsBOM:
    """
    物料BOM相关接口
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="MaterialsBOM").get_logger()
        self.url = get_url()

    def storeManufactureBomData(self,BOMVersion,BOMCode=BOMCode):
        """
        新增物料BOM
        :param BOMCode BOM编码
        :return: 响应实例体对象
        """
        from Toolbox.random_container import random_characters
        uploads =  {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "BOMCode": BOMCode,
            "IsUse": True,
            "OpSign": 1,
            "BOMVersion": BOMVersion,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreManufactureBomData = self.url + apiStoreManufactureBomData
        try:
            response = requests.post(url=urlStoreManufactureBomData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreManufactureBomData}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def getGetBomMasterViewAutoQueryDatas(self,MaterialCode=MaterialCode):
        """
        物料BOM查询接口
        :param MaterialCode: 物料代码
        :return: 响应实例体对象
        """
        uploads = {
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "IsPaged": True,
            "MaterialCode": MaterialCode,
        }
        try:
            urlGetBomMasterViewAutoQueryDatas = self.url + apiGetBomMasterViewAutoQueryDatas
            response = requests.post(url=urlGetBomMasterViewAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetBomMasterViewAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def storeBatchManufactureBomDetailDatas(self,BOMVersion):
        """
        新增物料BOM明细(绑定物料)
        """
        BOMBasicCode = BOMCode + '_' + BOMVersion
        uploads = [{
            "MaterialCode": "CQ01",
            "MaterialCategoryCode": "DQJ",
            "MaterialName": "多重加工测试物料",
            "MaterialSpecification": "",
            "MaterialDrawCode": None,
            "MaterialVersion": "",
            "MaterialUnit": "MU-01-CS",
            "MaterialAuxUnit": None,
            "MaterialAttribute": "SelfCreated",
            "MaterialProperty": "成品",
            "IsProduct": True,
            "IsSemiFinishedProduct": False,
            "IsMaterial": False,
            "IsUse": True,
            "DataSource": "",
            "MaintainerId": 10402,
            "MaintainerName": "CQ",
            "MaintainTime": "2025-06-23T11:03:45.323+08:00",
            "IsChecked": False,
            "CreatorUserId": 10402,
            "CreatorUserName": "CQ",
            "CreatorUserRealName": "陈强",
            "CreationTime": "2025-04-15T14:18:30.91+08:00",
            "LastModifierUserId": 10402,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "LastModificationTime": "2025-06-23T11:03:45.393+08:00",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Remark": "",
            "expand": False,
            "index": 1,
            "select": True,
            "check": True,
            "BOMBasicCode": BOMBasicCode
        }]
        try:
            urlStoreBatchManufactureBomDetailDatas = self.url + apiStoreBatchManufactureBomDetailDatas
            response = requests.post(url=urlStoreBatchManufactureBomDetailDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreBatchManufactureBomDetailDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None


    def removeManufactureBomData(self,BOMVersion,material_bom_id,BOMCode=BOMCode):
        """
        删除物料BOM 这个接口有点问题，信息都给了也提示删除成功了，实际没有删除成功
        :param BOMCode: BOM编码
        :param CompanyCode: 公司编码
        :return: 响应实例体对象
        """
        BOMBasicCode = BOMCode + '_' + BOMVersion
        uploads = {
            "MaterialName": MaterialName,
            "MaterialSpecification": "",
            "MaterialDrawCode": None,
            "MaterialAttribute": "SelfCreated",
            "MaterialUnit": None,
            "MaterialAuxUnit": None,
            "IsProduct": True,
            "IsSemiFinishedProduct": True,
            "IsMaterial": True,
            "BOMCode": BOMCode,
            "BOMBasicCode": BOMBasicCode,
            "BOMGroupCode": "",
            "MaterialCode": MaterialCode,
            "MaterialVersion": "",
            "BOMVersion": BOMVersion,
            "VaildStartDate": None,
            "VaildEndDate": None,
            "IsUse": True,
            "PurposeRemark": None,
            "CreatorUserId": 0,
            "CreatorUserName": "",
            "CreatorUserRealName": None,
            "CreationTime": "0001-01-01T00:00:00+08:00",
            "LastModifierUserId": None,
            "LastModifierUserName": None,
            "LastModifierUserRealName": None,
            "LastModificationTime": None,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": material_bom_id,
            "Remark": None,
            "typeTitle": "产",
            "typeTooltipTitle": "物料+半成品+成品"
        }
        urlRemoveManufactureBomData = self.url + apiRemoveManufactureBomData
        try:
            response = requests.post(url=urlRemoveManufactureBomData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveManufactureBomData}，请求头: {self.headers}，请求体: {uploads}")
            return None


if __name__ == '__main__':
    res1 = MaterialsBOM().getGetBomMasterViewAutoQueryDatas().json()
    ID = res1["Attach"][0]["Id"]
    res2 = MaterialsBOM().removeManufactureBomData("RUNL8249604",ID).json()
    # res = MaterialsBOM().storeBatchManufactureBomDetailDatas().json()
    # res1 = MaterialsBOM().removeManufactureBomData(279).json()
    print(f"物料BOMID为：{ID}")
    print(f"物料BOM查询：{res1}")
    print(f"删除物料BOM-请求体：{res2}")