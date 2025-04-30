import allure
from Business.mom_admin.login_mom_admin import LoginMomAdmin
from Toolbox.log_module import Logger
from markers import grade_1, grade_3
import pytest

logger = Logger(name="my_logger").get_logger()  # 实例化 Logger 类，获取日志记录器


@allure.feature("测试登录模块")
class TestLogin:
    """
    全平台登录相关用例
    """

    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("正确账号密码登陆")  # 在allure报告中自定义测试用例标题
    @allure.description("使用正确的账号和密码登录，登陆成功")  # 报告中测试用例的详细描述
    def test_login01(self):
        with allure.step("登录MOM管理端-验证是否登陆成功"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = LoginMomAdmin().login_mom_admin()  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_login01。获取到的结果是：{resBody['Message']}, 期望的结果是:数据更新成功，返回token")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "数据更新成功"  # 断言数据更新成功
            assert resBody['Attach']['AccessToken'] != {}  # 断言token非空
        except AssertionError as e:
            logger.error("登录页面：test_login01 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=3)  # 执行顺序
    @grade_3  # 优先级
    @allure.title("正确账号错误密码登陆")  # 在allure报告中自定义测试用例标题
    @allure.description("正确账号错误密码登陆，登陆失败并给出相应的提示")  # 报告中测试用例的详细描述
    def test_login02(self):
        with allure.step("登录MOM管理端-验证是否登陆成功"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = LoginMomAdmin().login_mom_admin(pass_word="222222132")  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_login02。获取到的结果是：{resBody['Message']}, 期望的结果是:账号错误，不返回token")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "密码错误"  # 断言数据提示
            assert resBody['Success'] == False  # 断言token非空
        except AssertionError as e:
            logger.error("登录页面：test_login02 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e

    @pytest.mark.run(order=3)  # 执行顺序
    @grade_3  # 优先级
    @allure.title("错误账号正确密码登陆")  # 在allure报告中自定义测试用例标题
    @allure.description("错误账号正确密码登陆，登陆失败并给出相应的提示")  # 报告中测试用例的详细描述
    def test_login03(self):
        with allure.step("登录MOM管理端-验证是否登陆成功"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = LoginMomAdmin().login_mom_admin(user_name="222222132")  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_login03。获取到的结果是：{resBody['Message']}, 期望的结果是:用户不存在，不返回token")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "用户不存在"  # 断言数据提示
            assert resBody['Success'] == False  # 断言token非空
        except AssertionError as e:
            logger.error("登录页面：test_login03 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e
