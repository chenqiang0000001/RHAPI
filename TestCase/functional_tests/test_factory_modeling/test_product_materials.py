import allure
from Business.mom_admin.factory_modeling.product_materials import ProductMaterials,MaterialsBOM,getGetBomMasterViewAutoQueryDatas
from Public.variables.mom_admin.factory_modeling import *
from Toolbox.log_module import Logger
from markers import grade_1, grade_3,grade_2
from Toolbox.delete_data import DataCleaner
import pytest


logger = Logger(name="TestProductMaterials").get_logger()  # 实例化 Logger 类，获取日志记录器


@allure.feature("物料相关模块")
class TestProductMaterials:
    """
    物料相关用例
    """

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("创建物料")  # 在allure报告中自定义测试用例标题
    @allure.description("使用符合要求的物料信息创建物料，创建成功")  # 报告中测试用例的详细描述
    def test_productaterials01(self):
        with allure.step("是否成功创建物料"):  # 在报告中记录测试用例中的测试步骤或详细信息
            DataCleaner().delete_data(1)  #自动清除数据-删除物料
            res = ProductMaterials().storeMaterialInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_productaterials01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 断言数据更新成功
            assert resBody['Attach']['MaterialCode'] == MaterialCode
        except AssertionError as e:
            logger.error("物料信息维护页面：test_productaterials01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("创建重复代码物料")  # 在allure报告中自定义测试用例标题
    @allure.description("创建重复代码物料，创建失败并给出相应的提示")  # 报告中测试用例的详细描述
    def test_productaterials02(self):
        with allure.step("是否成功创建物料"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProductMaterials().storeMaterialInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_productaterials02。获取到的结果是：{resBody['Message']}, 期望的结果是:已有重复数据录入!")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "已有重复数据录入!"
        except AssertionError as e:
            logger.error("物料信息维护页面：test_login01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("查询物料")  # 在allure报告中自定义测试用例标题
    @allure.description("使用已有的物料查询，查询成功")  # 报告中测试用例的详细描述
    def test_getMaterialInfoAutoQueryDatas01(self):
        with allure.step("是否成功test_getMaterialInfoAutoQueryDatas01查询物料"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProductMaterials().getMaterialInfoAutoQueryDatas() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_getMaterialInfoAutoQueryDatas01。获取到的结果是：{resBody['Message']}, 期望的结果是: 获取数据成功！")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "获取数据成功！"  # 断言数据查询成功
            assert resBody['Success'] is True
        except AssertionError as e:
            logger.error("物料信息维护页面：test_getMaterialInfoAutoQueryDatas01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("删除物料")  # 在allure报告中自定义测试用例标题
    @allure.description("使用已有的物料删除，删除成功")  # 报告中测试用例的详细描述
    def test_removeMaterialInfoData01(self):
        with allure.step("是否成功test_removeMaterialInfoData01删除物料"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = ProductMaterials().removeMaterialInfoData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_removeMaterialInfoData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 获取数据成功！")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 断言数据删除成功
            assert resBody['Success'] is True
        except AssertionError as e:
            logger.error("物料信息维护页面：test_removeMaterialInfoData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("新建物料BOM")  # 在allure报告中自定义测试用例标题
    @allure.description("新增已有的物料和不存在的BOM，新增成功")  # 报告中测试用例的详细描述
    def test_storeManufactureBomData01(self):
        with allure.step("是否成功test_storeManufactureBomData01新建物料BOM"):  # 在报告中记录测试用例中的测试步骤或详细信息
            ProductMaterials().storeMaterialInfoData()  # 新建物料
            res = MaterialsBOM().storeManufactureBomData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_storeManufactureBomData01。获取到的结果是：{resBody['Message']}, 期望的结果是: 数据新增成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据新增成功"  # 数据新增成功
            assert resBody['Attach']['BOMCode'] == BOMCode
            assert resBody['Success'] is True
        except AssertionError as e:
            logger.error("制造BOM页面：test_storeManufactureBomData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    # @pytest.mark.run(order=1)  # 执行顺序
    # @grade_2  # 优先级
    # @allure.title("新建重复物料BOM")  # 在allure报告中自定义测试用例标题
    # @allure.description("新增已有的物料和存在的BOM，新增失败并给出相应的提示")  # 报告中测试用例的详细描述
    # def test_storeManufactureBomData02(self):
    #     with allure.step("是否校验test_storeManufactureBomData02物料BOM版本"):  # 在报告中记录测试用例中的测试步骤或详细信息
    #         res = MaterialsBOM().storeManufactureBomData() # 实例登录接口
    #         resBody = res.json()  # 响应数据转化JSON
    #     logger.info(f"本用例正在执行：test_storeManufactureBomData02。获取到的结果是：{resBody['Message']}, 期望的结果是: BOM版本号【{BOMVersion}】已存在！请新增BOM版本号")  # 日志记录结果
    #     try:
    #         assert res.status_code == 200  # 断言响应状态码为200
    #         assert resBody['Message'] ==  f"BOM版本号【{BOMVersion}】已存在！请新增BOM版本号"  # 数据新增失败
    #     except AssertionError as e:
    #         logger.error("制造BOM页面：test_storeManufactureBomData01 断言失败，展开结果与预期不符")  # 错误日志记录
    #         raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("查询物料BOM")  # 在allure报告中自定义测试用例标题
    @allure.description("查询存在的物料BOM，数据正确")  # 报告中测试用例的详细描述
    def test_getGetBomMasterViewAutoQueryDatas01(self):
        with allure.step("查询test_getGetBomMasterViewAutoQueryDatas01物料BOM"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res =  getGetBomMasterViewAutoQueryDatas()# 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_getGetBomMasterViewAutoQueryDatas01。获取到的结果是：{resBody['Message']}, 期望的结果是:获取数据成功！")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "获取数据成功！"  # 获取数据成功！
            assert resBody['Attach'][0]['BOMCode'] == BOMCode
        except AssertionError as e:
            logger.error("制造BOM页面：test_getGetBomMasterViewAutoQueryDatas01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_2  # 优先级
    @allure.title("删除物料BOM")  # 在allure报告中自定义测试用例标题
    @allure.description("删除存在的物料BOM，删除成功")  # 报告中测试用例的详细描述
    def test_gremoveManufactureBomData01(self):
        with allure.step("删除test_gremoveManufactureBomData01物料BOM"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = MaterialsBOM().removeManufactureBomData() # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_gremoveManufactureBomData01。获取到的结果是：{resBody['Message']}, 数据删除成功")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] ==  "数据删除成功"  # 数据删除成功
            assert resBody['Success'] is True
            DataCleaner().delete_data(1)  # 自动清除数据-删除物料
        except AssertionError as e:
            logger.error("制造BOM页面：test_gremoveManufactureBomData01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e
