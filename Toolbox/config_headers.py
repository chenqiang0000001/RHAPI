import requests
import json
# 假设 Logger 类已经正确实现
from Toolbox.log_module import Logger
# 假设这些变量已经正确定义
from Public.variables.login import *
from Public.address.mom import get_url, apiGetMaterialInfoAutoQueryDatas, urlLogin1, apiLogin
import pytz
import tzlocal
from typing import Optional
import datetime

# 常用时区列表，可用于前端下拉选择
COMMON_TIMEZONES = [
    'Asia/Shanghai',  # 东八区
    'UTC',
    'Asia/Tokyo',
    'Asia/Seoul',
    'Europe/London',
    'Europe/Berlin',
    'America/New_York',
    'America/Los_Angeles',
    'Australia/Sydney',
    'Asia/Kolkata',
    'Asia/Bangkok',  # 东七区
    'Asia/Jakarta'   # 东七区
]
from Public.address.mom import (
    apiGetBomMasterViewAutoQueryDatas,
    apiGetProcessInfoAutoQueryDatas,
    apiGetProcessRoutingAutoQueryDatas,
    apiGetProductProcessRouteAutoQueryDatas
)


def get_token(pass_word=demo_password3, user_name=demo_username3, timezone: Optional[str] = None):
    """
    登录接口，获取有效的 authorization
    :param pass_word: 登录密码
    :param user_name: 登录账号
    :param timezone: 时区字符串，默认设备当前时区
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

    # 获取时区，默认本地时区，兜底Asia/Shanghai
    if timezone is None:
        try:
            timezone = tzlocal.get_localzone_name()
        except Exception:
            timezone = 'Asia/Shanghai'
    login_headers = {
        "X-Client-Timezone": timezone
    }

    while retries < max_retries:
        try:
            # 发送登录请求，带X-Client-Timezone头
            response = requests.post(url=urlLogin, json=login_data, headers=login_headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            token_type = data['Attach']['TokenType']
            access_token = data['Attach']['AccessToken']
            # 直接用空格拼接
            authorization = f"{token_type} {access_token}"
            
            # 尝试验证token，但设置超时和错误处理
            try:
                query_data = {}
                # 在get_token函数中替换url变量为get_url()
                url = get_url()
                urlGetMaterialInfoAutoQueryDatas = url + apiGetMaterialInfoAutoQueryDatas
                headers = {"Authorization": authorization}
                response = requests.post(url=urlGetMaterialInfoAutoQueryDatas, headers=headers, json=query_data, timeout=5)
                if response.status_code == 200:
                    return authorization
                else:
                    logger.warning(f"Token验证失败，状态码: {response.status_code}")
            except requests.Timeout:
                logger.warning("Token验证超时，但继续使用获取到的token")
                return authorization
            except requests.RequestException as e:
                logger.warning(f"Token验证请求失败: {e}，但继续使用获取到的token")
                return authorization
                
        except (KeyError, json.JSONDecodeError):
            logger.error("解析响应 JSON 数据时发生错误。")
        except requests.RequestException as e:
            logger.error(f"请求发生错误: {e}")
        retries += 1

    logger.error("多次尝试后仍无法获取有效的 authorization。")
    return None


def get_headers(timezone: Optional[str] = None, pass_word=demo_password3, user_name=demo_username3):
    """
    组装请求头，包含authorization和X-Client-Timezone
    :param timezone: 时区字符串，默认设备当前时区
    :param pass_word: 登录密码
    :param user_name: 登录账号
    :return: headers字典
    """
    authorization = get_token(pass_word=pass_word, user_name=user_name, timezone=timezone)
    if timezone is None:
        try:
            timezone = tzlocal.get_localzone_name()
        except Exception:
            timezone = 'Asia/Shanghai'  # 兜底默认东八区
    headers = {
        "authorization": authorization,
        "X-Client-Timezone": timezone
    }
    return headers


if __name__ == '__main__':
    res = get_headers()
    print(res)