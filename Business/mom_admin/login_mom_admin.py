import requests
import json
from Toolbox.log_module import Logger
from Public.address.mom import urlLogin1, apiLogin
from Public.variables.login import demo_password3, demo_username3


def get_token(pass_word=demo_password3, user_name=demo_username3):
    """
    登录接口，获取有效的 authorization
    :param pass_word: 登录密码
    :param user_name: 登录账号
    :return: 有效的 authorization
    """
    logger = Logger(name="get_token").get_logger()
    uploads = {
        "passWord": pass_word,
        "userCode": user_name
    }
    urlLogin = urlLogin1 + apiLogin
    max_retries = 3
    retries = 0

    while retries < max_retries:
        try:
            # 发送登录请求
            response = requests.post(url=urlLogin, json=uploads)
            response.raise_for_status()
            try:
                data = response.json()
                token_type = data['Attach']['TokenType']
                access_token = data['Attach']['AccessToken']
                # 直接用空格拼接
                authorization = f"{token_type} {access_token}"

                # 验证 authorization 的有效性
                validation_url = "your_validation_url"
                headers = {
                    "Authorization": authorization
                }
                validation_response = requests.get(validation_url, headers=headers)
                if validation_response.status_code == 200:
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
