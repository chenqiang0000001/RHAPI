import requests
from Public.address.login import url, apiLogin
from Public.variables.login import passWord, userCode


class Login:
    """
    登录相关接口
    """

    def login(seif, pass_word=passWord, user_code=userCode):
        """
        登录接口
        :param user_code: 登录账号
        :return:
        """
        uploads = {
            "passWord": pass_word,
            "userCode": user_code
        }
        urlLogin = url + apiLogin
        return requests.post(url=urlLogin, json=uploads)


if __name__ == '__main__':
    resBody = Login().login().json()
    print(resBody)
