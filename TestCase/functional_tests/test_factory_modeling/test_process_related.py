import allure
from Business.mom_admin.factory_modeling.production_process import ProcessRelated
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.log_module import Logger
from markers import grade_1, grade_3,grade_2
from Toolbox.delete_data import DataCleaner
import pytest

logger = Logger(name="TestProcessRelated").get_logger()  # 实例化 Logger 类，获取日志记录器


@allure.feature("工序相关模块")
class TestProcessRelated:
    """
    工序相关用例
    """
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
    @allure.title("创建工序")  # 在allure报告中自定义测试用例标题
    @allure.description("使用符合要求的信息创建工序，创建成功")  # 报告中测试用例的详细描述
    def test_storeProcessInfoData01(self):
        with allure.step("是否成功创建工序"):  # 在报告中记录测试用例中的测试步骤或详细信息
            DataCleaner().delete_data(2)
            res = ProcessRelated().storeProcessInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeProcessInfoData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
            assert resBody['Attach']['ProcessCode'] == ProcessCode
        except AssertionError as e:
            logger.error("创建工序接口：test_storeProcessInfoData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("创建工序校验重复")  # 在allure报告中自定义测试用例标题
    @allure.description("使用重复的工序代码，创建失败")  # 报告中测试用例的详细描述
    def test_storeProcessInfoData02(self):
        with allure.step("创建工序校验重复"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().storeProcessInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeProcessInfoData02。获取到的结果是：{resBody['Message']}, 期望的结果是: 已有重复数据录入!")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "已有重复数据录入!"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("创建工序接口：test_storeProcessInfoData02 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("删除工序")  # 在allure报告中自定义测试用例标题
    @allure.description("删除已存在的工序，删除成功")  # 报告中测试用例的详细描述
    def test_removeProcessInfoData01(self):
        with allure.step("删除工序"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().removeProcessInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_removeProcessInfoData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据删除成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("删除工序接口：test_removeProcessInfoData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("新增工艺路线")  # 在allure报告中自定义测试用例标题
    @allure.description("新增符合要求的工艺路线，新增成功")  # 报告中测试用例的详细描述
    def test_storeProcessRoutingData01(self):
        with allure.step("新增工艺路线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().storeProcessRoutingData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeProcessRoutingData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新增工艺路线接口：test_storeProcessRoutingData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("新增重复工艺路线")  # 在allure报告中自定义测试用例标题
    @allure.description("新增重复工艺路线，新增失败")  # 报告中测试用例的详细描述
    def test_storeProcessRoutingData02(self):
        with allure.step("新增工艺路线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().storeProcessRoutingData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeProcessRoutingData02。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("新增工艺路线接口：test_storeProcessRoutingData02 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("删除工艺路线")  # 在allure报告中自定义测试用例标题
    @allure.description("删除工艺路线，删除成功")  # 报告中测试用例的详细描述
    def test_removeProcessRoutingData01(self):
        with allure.step("删除工艺路线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().removeProcessRoutingData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_removeProcessRoutingData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据删除成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("删除工艺路线接口：test_removeProcessRoutingData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("工艺路线绑定工序")  # 在allure报告中自定义测试用例标题
    @allure.description("工艺路线绑定工序，绑定成功")  # 报告中测试用例的详细描述
    def test_adjustProcessRoutingEntry01(self):
        with allure.step("工艺路线是否成功绑定工序"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().adjustProcessRoutingEntry() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_adjustProcessRoutingEntry01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据保存成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据保存成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("工艺路线绑定工序接口：test_adjustProcessRoutingEntry01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("产品绑定工艺路线")  # 在allure报告中自定义测试用例标题
    @allure.description("产品绑定工艺路线，绑定成功")  # 报告中测试用例的详细描述
    def test_storeBatchProductProcessRouteDatas01(self):
        with allure.step("产品是否成功绑定工艺路线"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().storeProcessInfoData()  # 创建工序
            res = ProcessRelated().storeProcessRoutingData() # 新增工艺路线
            res = ProcessRelated().adjustProcessRoutingEntry() # 工艺路线绑定工序
            res = ProcessRelated().adjustProcessRoutingEntry() # 产品绑定工艺路线
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_adjustProcessRoutingEntry01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据保存成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据保存成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("产品绑定工艺路线接口：test_adjustProcessRoutingEntry01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("产品工序BOM绑定")  # 在allure报告中自定义测试用例标题
    @allure.description("产品工序BOM绑定，绑定成功")  # 报告中测试用例的详细描述
    def test_selectManufactureBom01(self):
        with allure.step("产品是否成功产品工序BOM绑定"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProcessRelated().SelectManufactureBom() # 产品绑定工艺路线
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_selectManufactureBom01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据保存成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据保存成功"  # 断言数据更新成功
        except AssertionError as e:
            logger.error("产品工序BOM绑定接口：test_selectManufactureBom01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e