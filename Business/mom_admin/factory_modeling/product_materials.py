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
        :param materialCharacteristic: 物料特性
        :return: 响应实例体对象
        """
        uploads =
        #     "MaterialCode": MaterialCode,
        #     "MaterialName": MaterialName,
        #     "materialCharacteristic": materialCharacteristic,
        #     "MaterialCategoryCode": "DQJ",
        #     "MaterialAttribute": "SelfCreated",
        #     "OpSign": 1,
        #     "MaintainerId": 10402,
        #     "MaintainerName": "CQ",
        #     "MaintainTime": "2025-05-08T00:32:55.588Z",
        #     "CompanyCode": "00000",
        #     "FactoryCode": "00000.00001"
        #
        # }
        {
            "MaterialCode": "222222",
            "MaterialName": "2222",
            "materialCharacteristic": [
                {
                    "label": "成品",
                    "value": "IsProduct",
                    "customData": {
                        "checked": true
                    },
                    "checked": true
                },
                {
                    "label": "半成品",
                    "value": "IsSemiFinishedProduct",
                    "customData": {
                        "checked": true
                    },
                    "checked": true
                },
                {
                    "label": "物料",
                    "value": "IsMaterial",
                    "customData": {
                        "checked": true
                    },
                    "checked": true
                }
            ],
            "MaterialCategoryCode": "WJJ",
            "MaterialAttribute": "SelfCreated",
            "MaterialSpecification": "",
            "MaterialDrawCode": null,
            "MaterialUnit": null,
            "MaterialAuxUnit": null,
            "MaterialVersion": "",
            "DataSource": "",
            "IsUse": true,
            "Remark": "",
            "OpSign": 1,
            "MaintainerId": 10418,
            "MaintainerName": "zdh01",
            "MaintainTime": "2025-05-08T01:19:28.158Z",
            "IsProduct": true,
            "IsSemiFinishedProduct": true,
            "IsMaterial": true,
            "CompanyCode": "00000",
            "FactoryCode": ""
        }
        urlStoreMaterialInfoData = url + apiStoreMaterialInfoData
        try:
            response = requests.post(url=urlStoreMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
            print(f"{uploads},{urlStoreMaterialInfoData}")
            return response
        except requests.RequestException as e:
            self.logger.error(f"请求发生错误: {e}，请求 URL: {urlStoreMaterialInfoData}，请求头: {self.headers}，请求体: {uploads}")
            return None


if __name__ == '__main__':
    res = ProductMaterials().storeMaterialInfoData()
    if res:
        res_body = res.json()
        print(f"{res_body}")
    else:
        print("请求失败，未获取到有效响应")
