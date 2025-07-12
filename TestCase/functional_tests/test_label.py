import pytest
import allure
from Business.pda.label_operation import LabelOperation
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters
from markers import grade_1


@allure.feature("标签管理")
class TestLabel:
    @classmethod
    def setup_class(cls):
        cls.logger = Logger(name="test_label").get_logger()
        cls.label_op = LabelOperation()
        cls.label_sn = random_characters()
        cls.split_body = {
            "SN": cls.label_sn,
            "SplitQty": 1,
            "FactoryCode": "00000.00001",
            "CompanyCode": "00000"
        }
        # 新建标签（如有必要，可在此处调用接口预置标签数据）

    @grade_1
    @allure.title("扫描标签")
    def test_01_scan_label(self):
        with allure.step("调用接口扫描标签"):
            response = self.label_op.scan_label(sn=self.label_sn)
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body

    @grade_1
    @allure.title("标签拆分")
    def test_02_label_split(self):
        with allure.step("调用接口拆分标签"):
            response = self.label_op.label_split(split_body=self.split_body)
        assert response is not None
        assert response.status_code == 200
        response_body = response.json()
        assert 'Success' in response_body 