import allure
from Business.login import Login
from Toolbox.log_module import Logger
from markers import grade_4, grade_3, grade_1, grade_2
import pytest

logger = Logger(name="my_logger").get_logger()  # 实例化 Logger 类，获取日志记录器


@allure.feature("测试登录模块")
class TestLogin:
    """
    登录相关用例
    """
    @pytest.mark.run(order=1)  # 执行顺序
    @grade_1  # 优先级
    @allure.title("正确账号密码登陆")  # 在allure报告中自定义测试用例标题
    # @allure.description("使用正确的账号和密码登录，登陆成功")  # 报告中测试用例的详细描述
    def test_login(self):
        with allure.step("登录MOM管理端-验证是否登陆成功"):  # 在报告中记录测试用例中的测试步骤或详细信息
            res = Login().login()  # 实例登录接口
            resBody = res.json()  # 响应数据转化JSON
        logger.info(f"本用例正在执行：test_login。获取到的结果是：{resBody['Message']}, 期望的结果是:数据更新成功，返回token")  # 日志记录结果
        try:
            assert res.status_code == 200  # 断言响应状态码为200
            assert resBody['Message'] == "数据更新成功"  # 断言数据更新成功
            assert resBody['Attach']['AccessToken'] != {}  # 断言token非空
        except AssertionError as e:
            logger.error("登录页面：test_login 断言失败，展开结果与预期不符")  # 错误日志记录
            raise e
