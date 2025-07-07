# import pytest
# import allure
# from Business.mom_admin.production_management.production_plan import ProductionPlan, ProductionScheduling
# from Toolbox.log_module import Logger
# from Toolbox.random_container import random_characters
#
# @allure.feature("生产计划与派工管理")
# class TestProductionPlan:
#     @classmethod
#     def setup_class(cls):
#         cls.logger = Logger(name="test_production_plan").get_logger()
#         cls.plan = ProductionPlan()
#         cls.scheduling = ProductionScheduling()
#         cls.plan_code = random_characters()
#         cls.plan_id = None
#         cls.dispatch_code = None
#         # 新建生产计划，获取ID
#         response = cls.plan.storeProductionPlanOrderData()
#         if response and response.status_code == 200:
#             query_resp = cls.plan.getProductionPlanOrderAutoQueryDatas(ProductionPlanCode=cls.plan_code)
#             if query_resp and query_resp.status_code == 200:
#                 query_body = query_resp.json()
#                 if query_body.get('Attach') and len(query_body['Attach']) > 0:
#                     cls.plan_id = query_body['Attach'][0]['Id']
#
#     @allure.title("创建生产计划")
#     def test_01_create_plan(self):
#         with allure.step("调用接口创建生产计划"):
#             response = self.plan.storeProductionPlanOrderData()
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#
#     @allure.title("查询生产计划")
#     def test_02_query_plan(self):
#         with allure.step("调用接口查询生产计划"):
#             response = self.plan.getProductionPlanOrderAutoQueryDatas(ProductionPlanCode=self.plan_code)
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#         if response_body.get('Attach') and len(response_body['Attach']) > 0:
#             TestProductionPlan.plan_id = response_body['Attach'][0]['Id']
#
#     @allure.title("确认生产计划")
#     def test_03_confirm_plan(self):
#         with allure.step("调用接口确认生产计划"):
#             response = self.plan.confirmBatchProductionPlanOrderDatas([{"ProductionPlanCode": self.plan_code}])
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#
#     @allure.title("下达生产计划")
#     def test_04_issue_plan(self):
#         with allure.step("调用接口下达生产计划"):
#             response = self.plan.issuedBatchProductionPlanOrderDatas([{"ProductionPlanCode": self.plan_code}])
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#
#     @allure.title("创建派工单")
#     def test_05_create_dispatch(self):
#         with allure.step("调用接口创建派工单"):
#             response = self.scheduling.createBatchProductionDispatchOrder([{"ProductionPlanCode": self.plan_code}])
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#
#     @allure.title("查询派工单")
#     def test_06_query_dispatch(self):
#         with allure.step("调用接口查询派工单"):
#             response = self.scheduling.getProductionDispatchOrderAutoQueryDatas({"ProductionPlanCode": self.plan_code})
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#
#     @allure.title("下达派工单")
#     def test_07_issue_dispatch(self):
#         with allure.step("调用接口下达派工单"):
#             response = self.scheduling.IssuedBatchProductionDispatchOrderDatas([{"ProductionPlanCode": self.plan_code}])
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True