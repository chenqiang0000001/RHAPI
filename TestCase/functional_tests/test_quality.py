import pytest
import allure
from Business.mom_admin.quality_control.QC_scheme import ProductInspectionPlan, InspectionSheet
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters

@allure.feature("质量检验管理")
class TestQuality:
    @classmethod
    def setup_class(cls):
        cls.logger = Logger(name="test_quality").get_logger()
        cls.QC = ProductInspectionPlan()
        cls.inspection_sheet = InspectionSheet()
        cls.schema_code = random_characters()
        cls.schema_id = None
        cls.inspect_order_code = None
        # 新建质检方案，获取ID
        response = cls.QC.createProductInspectSchemaData()
        if response and response.status_code == 200:
            query_resp = cls.QC.GetIpqcProductInspectSchemaDatas()
            if query_resp and query_resp.status_code == 200:
                query_body = query_resp.json()
                if query_body.get('Attach') and len(query_body['Attach']) > 0:
                    cls.schema_id = query_body['Attach'][0]['Id']

    # @allure.title("创建检验方案")
    # def test_01_create_inspect_schema(self):
    #     with allure.step("调用接口创建检验方案"):
    #         response = self.QC.createProductInspectSchemaData(SchemaCode=self.schema_code)
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Message'] in ["数据新增成功", "ok"]
    #     assert response_body['Success'] is True
    #
    # @allure.title("查询检验方案")
    # def test_02_query_inspect_schema(self):
    #     with allure.step("调用接口查询检验方案"):
    #         response = self.QC.getProductInspectSchemaAutoQueryDatas(SchemaCode=self.schema_code)
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Success'] is True
    #     if response_body.get('Attach') and len(response_body['Attach']) > 0:
    #         TestQuality.schema_id = response_body['Attach'][0]['Id']
    #
    # @allure.title("创建首检单")
    # def test_03_create_first_inspect_order(self):
    #     with allure.step("调用接口创建首检单"):
    #         response = self.inspection_sheet.createFirstInspectOrder(SchemaId=self.schema_id)
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Message'] in ["数据新增成功", "ok"]
    #     assert response_body['Success'] is True
    #     if response_body.get('Attach') and len(response_body['Attach']) > 0:
    #         TestQuality.inspect_order_code = response_body['Attach'][0]['InspectOrderCode']
    #
    # @allure.title("查询首检单")
    # def test_04_query_first_inspect_order(self):
    #     with allure.step("调用接口查询首检单"):
    #         response = self.inspection_sheet.getInspectOrderAutoQueryDatas(InspectOrderCode=self.inspect_order_code)
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Success'] is True
    #
    # @allure.title("删除检验方案")
    # def test_05_delete_inspect_schema(self):
    #     with allure.step("调用接口删除检验方案"):
    #         response = self.QC.removeProductInspectSchemaData(SchemaId=self.schema_id)
    #     assert response is not None
    #     assert response.status_code == 200
    #     response_body = response.json()
    #     assert response_body['Message'] in ["删除成功", "ok"]