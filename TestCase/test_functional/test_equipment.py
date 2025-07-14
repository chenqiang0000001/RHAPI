# import pytest
# import allure
# from Business.mom_admin.equipment_management.equipment_ledger_management import EquipmentLedgerManagement
# from Toolbox.log_module import Logger
# from Toolbox.random_container import random_characters
# import time
#
# @allure.feature("设备台账管理")
# class TestEquipment:
#     @classmethod
#     def setup_class(cls):
#         cls.logger = Logger(name="test_equipment").get_logger()
#         cls.equipment_ledger = EquipmentLedgerManagement()
#         cls.equipment_code = random_characters() + str(int(time.time() * 1000))
#         cls.equipment_name = cls.equipment_code_
#         cls.equipment_id = None
#         # 新建设备，获取ID
#         response = cls.equipment_ledger.storeEquipmentLedgerData(EquipmentCode=cls.equipment_code, EquipmentName=cls.equipment_name)
#         if response and response.status_code == 200:
#             query_resp = cls.equipment_ledger.getEquipmentLedgerAutoQueryDatas(EquipmentCode=cls.equipment_code, EquipmentName=cls.equipment_name)
#             if query_resp and query_resp.status_code == 200:
#                 query_body = query_resp.json()
#                 if query_body.get('Attach') and len(query_body['Attach']) > 0:
#                     cls.equipment_id = query_body['Attach'][0]['Id']
#
#     # @allure.title("新增设备台账")
#     # def test_01_add_equipment(self):
#     #     with allure.step("调用接口新增设备台账"):
#     #         response = self.equipment_ledger.storeEquipmentLedgerData(EquipmentCode=self.equipment_code, EquipmentName=self.equipment_name)
#     #     assert response is not None
#     #     assert response.status_code == 200
#     #     response_body = response.json()
#     #     assert response_body['Success'] is True, f"设备新增失败: {response.text}"
#
#     @allure.title("查询设备台账")
#     def test_02_query_equipment(self):
#         with allure.step("调用接口查询设备台账"):
#             response = self.equipment_ledger.getEquipmentLedgerAutoQueryDatas(EquipmentCode=self.equipment_code, EquipmentName=self.equipment_name)
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert response_body['Success'] is True
#         if response_body.get('Attach') and len(response_body['Attach']) > 0:
#             TestEquipment.equipment_id = response_body['Attach'][0]['Id']
#
#     @allure.title("设备台账唯一性校验")
#     def test_03_equipment_uniqueness(self):
#         with allure.step("重复创建设备台账，期望失败"):
#             response = self.equipment_ledger.storeEquipmentLedgerData(EquipmentCode=self.equipment_code, EquipmentName=self.equipment_name)
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert 'Success' in response_body
#
#     @allure.title("删除设备台账")
#     def test_04_delete_equipment(self):
#         with allure.step("调用接口删除设备台账"):
#             response = self.equipment_ledger.removeBatchEquipmentLedger(TestEquipment.equipment_id)
#         assert response is not None
#         assert response.status_code == 200
#         response_body = response.json()
#         assert 'Success' in response_body