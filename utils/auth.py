
from django.http import JsonResponse

from backend import settings
from utils.response import wrap_json_response, ReturnCode

import requests
import json
from functools import wraps

def c2s(appid, code):
    return code2session(appid, code)


def code2session(appid, code):
    """
    获取微信用户的open_id
    :param appid: 小程序的appid
    :param code: 小程序的code
    :return: data data中储存请求到的参数
    """
    API = "https://api.weixin.qq.com/sns/jscode2session?"
    params = "appid={}&secret={}&js_code={}&grant_type=authorization_code".format(appid, settings.WX_SECRET, code)
    url = API + "?" + params
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data


def id_cert(name, id_number):
    pass


def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            is_authorized = requests.session().get('is_authorized')
        except Exception:
            response = wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response, safe=False)

        if not is_authorized:
            response = wrap_json_response(code=ReturnCode.UNAUTHORIZED)
            return JsonResponse(data=response, safe=False)
        return func(*args, **kwargs)

    return inner


def phone_cert(phone_nuber, captcha):
    pass