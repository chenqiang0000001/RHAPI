import allure
from Business.mom_admin.equipment_management.equipment_ledger_management import EquipmentLedgerManagement
from Toolbox.log_module import Logger
from markers import grade_1, grade_2
from Toolbox.delete_data import DataCleaner
import pytest

logger = Logger(name="TestEquipmentLedger").get_logger()  # 实例化 Logger 类，获取日志记录器
@allure.feature("设备台账模块")
class TestEquipmentLedger:

    @classmethod
    # def setup_class(cls):
    #     DataCleaner().clean_related_data()
    #
    # @classmethod
    #
    # def teardown_class(cls):
    #     DataCleaner().clean_related_data()

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("新建设备")  # 在allure报告中自定义测试用例标题
    @allure.description("使用符合要求的信息新建设备，新建成功")  # 报告中测试用例的详细描述
    def test_storeEquipmentLedgerData01(self):
        with allure.step("是否成功新建设备"):  # 在报告中记录测试用例中的测试步骤或详细信息
            DataCleaner().delete_data(4)  # 新增前删除设备台账数据
            res = EquipmentLedgerManagement().storeEquipmentLedgerData()  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(
            f"本用例正在执行：test_storeEquipmentLedgerData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "数据新增成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新建设备页面：test_storeEquipmentLedgerData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("新建设备校验唯一")  # 在allure报告中自定义测试用例标题
    @allure.description("使用重复的信息新建设备，新建失败")  # 报告中测试用例的详细描述
    def test_storeEquipmentLedgerData02(self):
        with allure.step("新建设备校验唯一"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = EquipmentLedgerManagement().storeEquipmentLedgerData()  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(
            f"本用例正在执行：test_storeEquipmentLedgerData02。获取到的结果是：{resBody['Message']}, 期望的结果是: 已有重复数据录入!")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "已有重复数据录入!"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新建设备接口：test_storeEquipmentLedgerData02 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("删除设备")  # 在allure报告中自定义测试用例标题
    @allure.description("删除设备，删除成功")  # 报告中测试用例的详细描述
    def test_removeBatchEquipmentLedger01(self):
        with allure.step("删除设备"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = EquipmentLedgerManagement().storeEquipmentLedgerData()  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(
            f"本用例正在执行：test_removeBatchEquipmentLedger01。获取到的结果是：{resBody['Message']}, 期望的结果是: 已有重复数据录入!")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "已有重复数据录入!"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("删除设备接口：test_removeBatchEquipmentLedger01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e