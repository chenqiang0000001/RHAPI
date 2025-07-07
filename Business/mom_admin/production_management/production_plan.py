import requests
from Public.address.mom import *
from Toolbox.log_module import Logger
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.get_token import get_token

class ProductionPlan:
    """
    生产计划相关接口
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="FactoryModel").get_logger()

    def storeProductionPlanOrderData(self):
        """
        新建生产计划单
        """
        uploads = {
            "ProductCode": MaterialCode,
            "ProductName": MaterialName,
            "OrganizationStructureCode": OrganizationStructureCode,
            "OrganizationStructureName": OrganizationStructureName,
            "PlanDateRange": ["2025-06-24", "2028-08-31"],
            "ProductionType": "Normal",
            "ProcessRoutingCode": ProcessRoutingCode2,
            "BOMCode": BOMCode,
            "BOMBasicCode": BOMCode,
            "ProcessRoutingName": ProcessRoutingName,
            "OpSign": 1,
            "PlanStartDate": "2025-06-24",
            "PlanEndDate": "2025-08-31",
            "CompanyCode": CompanyCode,
            "FactoryCode": "00000.00001",
            "PlanQty": PlanQty,  # 强制用有效数量
            # 其它参数如需补充可在此处加
        }
        self.logger.info(f"请求体: {uploads}")
        try:
            response = requests.post(url=url + apiStoreProductionPlanOrderData, headers=self.headers, json=uploads)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

    def getProductionPlanOrderAutoQueryDatas(self,ProductionPlanCode):
        """
        查询生产计划单(计划和调度通用查询接口)
        :param ProductionPlanCode: 生产计划单编码
        """
        uploads = {
            "ProductionPlanCode": [ProductionPlanCode],  # 改为数组格式
        }
        urlGetProductionPlanOrderAutoQueryDatas = url + apiGetProductionPlanOrderAutoQueryDatas
        try:
            response = requests.post(url=urlGetProductionPlanOrderAutoQueryDatas, headers=self.headers, json=uploads)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(
                f"请求发生错误: {e}，请求 URL: {urlGetProductionPlanOrderAutoQueryDatas}，请求头: {self.headers}，请求体: {uploads}")
            raise e

    def confirmBatchProductionPlanOrderDatas(self, plan_data_list):
        """
        计划单确认，参数为列表
        """
        urlConfirmBatchProductionPlanOrderDatas = url + apiConfirmBatchProductionPlanOrderDatas
        self.logger.info(f"请求体: {plan_data_list}")
        try:
            response = requests.post(url=urlConfirmBatchProductionPlanOrderDatas, headers=self.headers, json=plan_data_list)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

    def issuedBatchProductionPlanOrderDatas(self, plan_data_list):
        """
        计划单下达，参数为列表
        """
        urlIssuedBatchProductionPlanOrderDatas = url + apiIssuedBatchProductionPlanOrderDatas
        self.logger.info(f"请求体: {plan_data_list}")
        try:
            response = requests.post(url=urlIssuedBatchProductionPlanOrderDatas, headers=self.headers, json=plan_data_list)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

class ProductionScheduling:
    """
    生产调度相关接口
    """
    def __init__(self):
        authorization = get_token()
        self.headers = {
            "authorization": authorization
        }
        self.logger = Logger(name="ProductionScheduling").get_logger()

    def createBatchProductionDispatchOrder(self, dispatch_data_list):
        """
        快捷派工，参数为列表
        """
        urlCreateBatchProductionDispatchOrderData = url + apiCreateBatchProductionDispatchOrderData
        self.logger.info(f"请求体: {dispatch_data_list}")
        try:
            response = requests.post(url=urlCreateBatchProductionDispatchOrderData, headers=self.headers, json=dispatch_data_list)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

    def IssuedBatchProductionDispatchOrderDatas(self, dispatch_data_list):
        """
        派工单下达，参数为列表
        """
        urlIssuedBatchProductionDispatchOrderDatas = url + apiIssuedBatchProductionDispatchOrderDatas
        self.logger.info(f"请求体: {dispatch_data_list}")
        try:
            response = requests.post(url=urlIssuedBatchProductionDispatchOrderDatas, headers=self.headers, json=dispatch_data_list)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

    def getCanDispatchProcessTaskOrderDatas(self, body):
        """
        查询可派工的工序任务单
        :param body: 查询参数dict，需包含ProductionPlanCode等
        :return: requests响应对象
        """
        url_get = url + "ProductionDispatchApi/GetCanDispatchProcessTaskOrderDatas"
        self.logger.info(f"请求体: {body}")
        try:
            response = requests.post(url=url_get, headers=self.headers, json=body)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None

    def getProductionDispatchOrderAutoQueryDatas(self, body):
        """
        查询派工单（用计划单号等条件）
        :param body: 查询参数dict，需包含ProductionPlanCode等
        :return: requests响应对象
        """
        url_get = url + "ProductionDispatchApi/GetProductionDispatchOrderAutoQueryDatas"
        self.logger.info(f"请求体: {body}")
        try:
            response = requests.post(url=url_get, headers=self.headers, json=body)
            self.logger.info(f"响应体: {getattr(response, 'text', response)}")
            return response
        except Exception as e:
            self.logger.error(f"请求发生错误: {e}")
            return None