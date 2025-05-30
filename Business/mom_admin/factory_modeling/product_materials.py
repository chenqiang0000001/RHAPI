import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token


class ProductMaterials:
    """
    产品物料相关接口封装
    """

    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="ProductMaterials").get_logger()

    def storeMaterialInfoData(self, MaterialCode=MaterialCode, MaterialName=MaterialName,
                              materialCharacteristic=materialCharacteristic):
        """
        新增产品物料
        :param MaterialCode: 物料编码
        :param MaterialName: 物料名称
        :param MaterialProperty: 物料特性
        :return: MaterialAttribute:物料属性
        :return: 响应实例体对象
        """
        uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "materialCharacteristic": [{
                "label": "成品",
                "value": "IsProduct"
            }, {
                "label": "半成品",
                "value": "IsSemiFinishedProduct"
            }, {
                "label": "物料",
                "value": "IsMaterial",
            }],
            "MaterialCategoryCode": "DQJ",
            "MaterialAttribute": "SelfCreated",
            "OpSign": 1,
            "MaintainerId": 10402,
            "MaintainerName": "CQ",
            "MaintainTime": "2025-05-20T02:53:17.745Z",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStoreMaterialInfoData = url + apiStoreMaterialInfoData
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
        urlGetMaterialInfoAutoQueryDatas = url + apiGetMaterialInfoAutoQueryDatas
        try:
            response = requests.post(url=urlGetMaterialInfoAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlGetMaterialInfoAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            return None

    def removeMaterialInfoData(self,MaterialCode=MaterialCode,MaterialName=MaterialName):
        """
        删除物料
        :param MaterialCode: 物料编码
        :param MaterialName: 物料名称
        :return: 响应实例体对象
        """
        uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
        }
        urlRemoveMaterialInfoData = url + apiRemoveMaterialInfoData
        try:
            response = requests.post(url=urlRemoveMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveMaterialInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None

def getGetBomMasterViewAutoQueryDatas(MaterialCode=MaterialCode):
    """
    物料BOM查询接口
    :param MaterialCode: 物料代码
    :return:物料BOM ID
    """
    logger = Logger(name="getGetBomMasterViewAutoQueryDatas").get_logger()
    authorization = get_token()
    headers = {
        "authorization": authorization
    }
    uploads = {
        "CompanyCode":CompanyCode,
        "MaterialCode": MaterialCode,
    }
    try:
        urlGetBomMasterViewAutoQueryDatas = url + apiGetBomMasterViewAutoQueryDatas
        response = requests.post(url=urlGetBomMasterViewAutoQueryDatas, headers=headers, json=uploads)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logger.error(
            f"请求发生错误: {e}，请求 URL: {urlGetBomMasterViewAutoQueryDatas}，请求头: {headers}，请求体: {uploads}")
        return None

class MaterialsBOM:
    """
    物料BOM相关接口
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="MaterialsBOM").get_logger()

    def storeManufactureBomData(self,BOMCode=BOMCode):
        """
        新增物料BOM
        :param BOMCode BOM编码
        :return: 响应实例体对象
        """
        from Toolbox.random_container import random_characters
        BOMVersion = random_characters()  #获取随机版本号
        uploads = {
                "MaterialCode": MaterialCode,
                "MaterialName": MaterialName,
                "BOMCode": BOMCode,
                "BOMVersion": BOMVersion,
                "MaterialSpecification": "",
                "OpSign": 1,
                "CompanyCode": "00000",
                "FactoryCode": "00000.00001"
        }
        urlStoreManufactureBomData = url + apiStoreManufactureBomData
        try:
            response = requests.post(url=urlStoreManufactureBomData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStoreManufactureBomData}，请求头: {self.headers}，请求体: {uploads}")
            return None


    def removeManufactureBomData(self,BOMCode=BOMCode,CompanyCode=CompanyCode):
        """
        删除物料BOM 这个接口有点问题，信息都给了也提示删除成功了，实际没有删除成功
        :param BOMCode: BOM编码
        :param CompanyCode: 公司编码
        :return: 响应实例体对象
        """
        resBody = getGetBomMasterViewAutoQueryDatas().json()
        id = resBody["Attach"][0]["Id"]#获取物料BOM ID
        uploads = {
            "BOMCode": BOMCode,
            "BOMBasicCode": "Automation001_520",
            "BOMGroupCode": "",
            "MaterialCode": MaterialCode,
            "BOMVersion": "520",
            "CreatorUserId": 0,
            "CreatorUserName": "",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
            "NeedUpdateFields": {},
            "Id": id,
            "typeTooltipTitle": "",
            "index": 1,
        }
        urlRemoveMaterialInfoData = url + apiRemoveMaterialInfoData
        try:
            response = requests.post(url=urlRemoveMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlRemoveMaterialInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None


if __name__ == '__main__':
    res = MaterialsBOM().removeManufactureBomData().json()
    # res = MaterialsBOM().removeManufactureBomData().json()
    print(f"{res}")