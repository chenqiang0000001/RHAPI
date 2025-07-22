import requests
from Public.address.mom import get_url, urlLogin1, apiLogin
from Public.variables.login import *
from Toolbox.log_module import Logger


class LoginMomAdmin:
    """
    mom登录相关接口
    """

    def __init__(self):
        self.logger = Logger(name="my_logger").get_logger()

    def login_mom_admin(self, pass_word=demo_password2, user_name=demo_username2):
        """
        登录接口
        :param pass_word: 登录密码
        :param user_name: 登录账号
        :return: 登陆信息
        """
        uploads = {
            "passWord": pass_word,
            "userCode": user_name
        }
        urlLogin = urlLogin1 + apiLogin
        try:
            response = requests.post(url=urlLogin, json=uploads)
            response.raise_for_status()  # 若状态码不在 200 - 299 范围内，抛出 HTTPError 异常
            return response
        except requests.RequestException as e:
            self.logger.error(f"登录请求发生错误: {e}，请求URL: {urlLogin}，请求体: {uploads}")
            return None


if __name__ == '__main__':
    resBody = LoginMomAdmin().login_mom_admin()
    print(resBody)
