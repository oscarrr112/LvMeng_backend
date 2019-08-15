class ReturnCode:

    # 公用状态码
    SUCCESS = 0
    FAILED = 100
    UNAUTHORIZED = 101
    BROKEN_PARAMS = 102

    # 验证登录状态码
    WRONG_CODE = 201
    FREQUENCY_LIMITED = 202

    # 实名验证状态码
    WRONG_NAME_FORM = 203
    WRONG_ID_FORM = 204
    MATCH_FAIL = 205
    NO_ID = 206

    # 手机绑定状态码
    WRONG_PHONE_NUMBER = 207
    WRONG_CAPTCHA = 208
    CAPTCHA_DUE = 209


messages = dict()

# 公用状态信息
messages[ReturnCode.SUCCESS] = '请求成功'
messages[ReturnCode.FAILED] = '系统繁忙，请重试'
messages[ReturnCode.UNAUTHORIZED] = '未登录'

# 验证登录状态信息
messages[ReturnCode.BROKEN_PARAMS] = '参数不完整'
messages[ReturnCode.WRONG_CODE] = '无效的code'
messages[ReturnCode.FREQUENCY_LIMITED] = '频率限制，每个用户每分钟100次'

# 实名验证状态信息
messages[ReturnCode.WRONG_NAME_FORM] = '开户名不能包含特殊字符'
messages[ReturnCode.WRONG_ID_FORM] = '身份证号格式错误'
messages[ReturnCode.MATCH_FAIL] = '身份证信息不匹配'
messages[ReturnCode.NO_ID] = '该身份证号码不存在'

# 手机绑定状态信息
messages[ReturnCode.WRONG_PHONE_NUMBER] = '手机号不正确'
messages[ReturnCode.WRONG_CAPTCHA] = '验证码错误'
messages[ReturnCode.CAPTCHA_DUE] = '验证码过期'


class CommonResponseMixin(object):
    @classmethod
    def wrap_json_response(cls, data=None, code=None, message=None):
        response = wrap_json_response(data, code, message)
        return response


def wrap_json_response(data=None, code=None, message=None):
    response = {}
    if not code:
        code = ReturnCode.SUCCESS
    if not message:
        message = messages[code]

    if data is not None:
        for key, val in data.items:
            response[key] = val
    response['result_code'] = code
    response['message'] = message
    return response
