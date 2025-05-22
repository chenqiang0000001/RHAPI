import requests
import json
# 假设 Logger 类已经正确实现
from Toolbox.log_module import Logger
# 假设这些变量已经正确定义
from Public.variables.login import demo_password3, demo_username3
from Public.address.mom import *


def get_token(pass_word=demo_password3, user_name=demo_username3):
    """
    登录接口，获取有效的 authorization
    :param pass_word: 登录密码
    :param user_name: 登录账号
    :return: 有效的 authorization
    """
    logger = Logger(name="get_token").get_logger()
    login_data = {
        "passWord": pass_word,
        "userCode": user_name
    }
    urlLogin = urlLogin1 + apiLogin
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # 发送登录请求
            response = requests.post(url=urlLogin, json=login_data)
            response.raise_for_status()
            data = response.json()
            token_type = data['Attach']['TokenType']
            access_token = data['Attach']['AccessToken']
            # 直接用空格拼接
            authorization = f"{token_type} {access_token}"
            # 后续请求的数据
            query_data = {}
            urlGetMaterialInfoAutoQueryDatas = url + apiGetMaterialInfoAutoQueryDatas
            # headers 参数需要传入字典
            headers = {"Authorization": authorization}
            response = requests.post(url=urlGetMaterialInfoAutoQueryDatas, headers=headers, json=query_data)
            if response.status_code == 200:
                return authorization
            else:
                logger.warning("当前 authorization 无效，尝试重新获取...")
        except (KeyError, json.JSONDecodeError):
            logger.error("解析响应 JSON 数据时发生错误。")
        except requests.RequestException as e:
            logger.error(f"请求发生错误: {e}")
        retries += 1

    logger.error("多次尝试后仍无法获取有效的 authorization。")
    return None


if __name__ == '__main__':
    res = get_token()
    print(res)
