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
        :param materialCharacteristic: 物料属性配置
        :return: 响应实例体对象
        """
        uploads = {
            "MaterialCode": MaterialCode,
            "MaterialName": MaterialName,
            "materialCharacteristic": materialCharacteristic,
            "MaterialCategoryCode": "DQJ",
            "MaterialAttribute": "SelfCreated",
            "MaterialSpecification": "",
            "OpSign": 1,
            "MaintainerId": 10402,
            "MaintainerName": "CQ"
        }
        urlStoreMaterialInfoData = url + apiStoreMaterialInfoData
        try:
            response = requests.post(url=urlStoreMaterialInfoData, headers=self.headers, json=uploads)
            response.raise_for_status()
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
        print("请求失败，未获取到有效响应。")

