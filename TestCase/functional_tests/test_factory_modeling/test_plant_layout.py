import allure
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials,MaterialsBOM,getGetBomMasterViewAutoQueryDatas
from Business.mom_admin.production_modeling.factory_model import FactoryModel
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.log_module import Logger
from Toolbox.random_container import random_characters
from markers import grade_1, grade_3,grade_2
from Toolbox.delete_data import DataCleaner
import pytest


logger = Logger(name="PlantLayout").get_logger()  # 实例化 Logger 类，获取日志记录器


@allure.feature("车间布局相关模块")
class TestPlantLayout:
    OrganizationStructureCode = None

    @classmethod
    def setup_class(cls):
        cls.OrganizationStructureCode = random_characters()

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("新增车间")  # 在allure报告中自定义测试用例标题
    @allure.description("使用符合要求的信息创建车间，创建成功")  # 报告中测试用例的详细描述
    def test_storeOrganizationStructureData01(self):
        with allure.step("是否成功创建车间"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = FactoryModel().storeOrganizationStructureData(OrganizationStructureCode=self.OrganizationStructureCode) # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeOrganizationStructureData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新增车间接口：test_storeOrganizationStructureData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_3  # 优先级
    @allure.title("创建重复车间")  # 在allure报告中自定义测试用例标题
    @allure.description("使用重复的信息创建车间，创建失败")  # 报告中测试用例的详细描述
    def test_storeOrganizationStructureData02(self):
        with allure.step("不可重复创建车间"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = FactoryModel().storeOrganizationStructureData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeOrganizationStructureData02。获取到的结果是：{resBody['Message']}")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "不能在具有唯一索引“OrganizationStructureCode”的对象“dbo.FactoryLayout_OrganizationStructure”中插入重复键的行。重复键值为 (Automation01)。\r\n语句已终止。"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("物料信息维护页面：test_productaterials01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("删除车间")  # 在allure报告中自定义测试用例标题
    @allure.description("删除存在的车间，删除成功")  # 报告中测试用例的详细描述
    def test_removeOrganizationStructureData01(self):
        with allure.step("是否成功删除车间"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = FactoryModel().removeOrganizationStructureData(OrganizationStructureCode=self.OrganizationStructureCode) # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_removeOrganizationStructureData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据删除成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("删除车间接口：test_removeOrganizationStructureData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("新增产线")  # 在allure报告中自定义测试用例标题
    @allure.description("使用符合要求的信息创建产线，创建成功")  # 报告中测试用例的详细描述
    def test_storeOrganizationStructureData_productionline01(self):
        with allure.step("是否成功创建产线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            OrganizationStructureCode = random_characters()
            res = FactoryModel().storeOrganizationStructureData_productionline(OrganizationStructureCode2=OrganizationStructureCode) # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeOrganizationStructureData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新增车间接口：test_storeOrganizationStructureData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_3  # 优先级
    @allure.title("创建重复产线")  # 在allure报告中自定义测试用例标题
    @allure.description("使用重复的物料信息创建产线，创建失败")  # 报告中测试用例的详细描述
    def test_storeOrganizationStructureData_productionline02(self):
        with allure.step("是否能重复创建产线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = FactoryModel().storeOrganizationStructureData_productionline() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeOrganizationStructureData_productionline02。获取到的结果是：{resBody['Message']}")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "不能在具有唯一索引“OrganizationStructureCode”的对象“dbo.FactoryLayout_OrganizationStructure”中插入重复键的行。重复键值为 (Automation01)。\r\n语句已终止。"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("物料信息维护页面：test_productaterials01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("删除产线")  # 在allure报告中自定义测试用例标题
    @allure.description("删除存在的产线，删除成功")  # 报告中测试用例的详细描述
    def test_removeOrganizationStructureData_productionline01(self):
        with allure.step("是否成功删除产线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = FactoryModel().removeOrganizationStructureData_productionline() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_removeOrganizationStructureData_productionline01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据删除成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("删除车间接口：test_removeOrganizationStructureData_productionline01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e