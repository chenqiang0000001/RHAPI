import requests
from Public.address.mom import get_url, apiCreateProductInspectSchemaData, apiGetIpqcProductInspectOrderDatas, \
    apiStartInspectProcessInspectOrder, apiSubmitProcessInspectOrderData
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.config_headers import get_headers

class ProductInspectionPlan:
    """
    产品检验方案相关接口
    """
    def __init__(self):
        authorization = get_headers()["authorization"]
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="FactoryModel").get_logger()
        self.url = get_url()

    def createProductInspectSchemaData(self):
        """
        新增产品检验方案
        """
        uploads = {

                "ProductCode":MaterialCode,
                "ProductName": MaterialName,
                "ProductSpecification": "",
                "ProductDrawCode": "",
                "ProcessRoutingCode": ProcessRoutingCode2,
                "ProcessCode": ProcessCode,
                "ValidDateRange": ["2025-06-01", "2030-08-03"],
                "IsUse": True,
                "IsTimingStart": False,
                "Minute": 0,
                "Remark": "",
                "ProcessRoutingName": ProcessCode,
                "ProcessName": ProcessName,
                "OpSign": 1,
                "SpecialInspect": False,
                "FirstInspect": True,
                "ProfessionalInspect": False,
                "SampleInspect": False,
                "PatrolInspect": False,
                "RegularInspect": False,
                "EndInspect": False,
                "ValidStartDate": "2025-06-01",
                "ValidEndDate": "2030-08-03",
                "SelectedProcess": [{
                    "ProductCode": MaterialCode,
                    "ProductName": MaterialName,
                    "ProcessRoutingCode":ProcessRoutingCode2,
                    "ProcessRoutingEntryCode": "0f9cac55-5ab6-4036-9678-9a2151c1ce46",
                    "LastProcessRoutingEntryCode": "68564a88-0c36-4830-b7b3-56d084a32554",
                    "NextProcessRoutingEntryCode": "",
                    "ProcessCode": ProcessCode,
                    "ProcessName": ProcessName,
                    "ProcessSeq": 3,
                    "OrganizationStructureCode": OrganizationStructureParentCode,
                    "OrganizationStructureName": OrganizationStructureName,
                    "OrganizationStructureExternalCode": OrganizationStructureCode,
                }],
                "CompanyCode": "00000",
                "FactoryCode": "00000.00001"
            }
        urlCreateProductInspectSchemaData = self.url + apiCreateProductInspectSchemaData
        try:
            response = requests.post(url=urlCreateProductInspectSchemaData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlCreateProductInspectSchemaData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def GetIpqcProductInspectSchemaDatas(self):
        """
        查询产品检验方案
        """
        uploads = {
                "ProductCode": MaterialCode,
                "CompanyCode": "00000",
                "FactoryCode": "00000.00001"
        }
        urlCreateProductInspectSchemaData = self.url + apiCreateProductInspectSchemaData
        try:
            response = requests.post(url=urlCreateProductInspectSchemaData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlCreateProductInspectSchemaData}，请求头: {self.headers}，请求体: {uploads}")
            raise e

class InspectionSheet:
    """
    检验任务单相关接口
    """
    def __init__(self, timezone=None):
        self.headers = get_headers(timezone=timezone)
        self.logger = Logger(name="FactoryModel").get_logger()
        self.url = get_url()

    def getIpqcProductInspectOrderDatas(self,ProductionPlanCode):
        """
        查询检验任务单
        :productionplancode:生产计划编码
        """
        uploads = {
            "ProductionPlanCode": ProductionPlanCode,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlGetIpqcProductInspectOrderDatas = self.url + apiGetIpqcProductInspectOrderDatas
        try:
            response = requests.post(url=urlGetIpqcProductInspectOrderDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetIpqcProductInspectOrderDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def startInspectProcessInspectOrder(self,InspectOrderCode,inspection_sheet_id):
        """
        开始校验
        :param InspectOrderCode: 检验任务单编码
        :param inspection_sheet_id: 检验任务单id
        """
        uploads = {
            "InspectOrderCode": InspectOrderCode,
            "id": inspection_sheet_id,
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001"
        }
        urlStartInspectProcessInspectOrder = self.url + apiStartInspectProcessInspectOrder
        try:
            response = requests.post(url=urlStartInspectProcessInspectOrder, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlStartInspectProcessInspectOrder}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def submitProcessInspectOrderData(self,InspectOrderCode,ProductionDispatchCode,ProductionPlanCode,inspection_sheet_id):
        """
        提交检验任务单
        :param InspectOrderCode: 检验任务单编码
        :param ProductionDispatchCode: <UNK>     派工单编码
        :param ProductionPlanCode: <UNK>    计划单号
        """
        uploads = {
            "InspectOrderCode": InspectOrderCode,
            "ProductionDispatchCode": ProductionDispatchCode,
            "ProductionPlanCode": ProductionPlanCode,
            "InspectCategory": "FirstInspect",
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "id": inspection_sheet_id,
            "ProcessRoutingCode": "CQ-GX-1",
            "ProcessRoutingName": "CQ-GX",
            "OrderStatus": "Inspecting",
            "ControlStatus": "Enable",
            "SendInspectQty": 7,
            "SendInspectorCode": "CQ",
            "SendInspectorName": "CQ",
            "GoodQty": 7,
            "BadQty": 0,
            "ScrappedQty": 0,
            "ConcessionReceiveQty": 0,
            "LastModifierUserName": "CQ",
            "LastModifierUserRealName": "陈强",
            "CompanyCode": "00000",
            "FactoryCode": "00000.00001",
        }
        urlSubmitProcessInspectOrderData = self.url + apiSubmitProcessInspectOrderData
        try:
            response = requests.post(url=urlSubmitProcessInspectOrderData, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlSubmitProcessInspectOrderData}，请求头: {self.headers}，请求体: {uploads}")
            raise e


if __name__ == '__main__':
    res = ProductInspectionPlan().createProductInspectSchemaData().json()
    # res2 = ProductInspectionPlan().GetIpqcProductInspectSchemaDatas().json()
    # print(res)
    print(res)