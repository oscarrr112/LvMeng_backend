"""
@author 彭奥
授权相关视图函数


下一步改进：
1. 实现更改手机绑定
2. 未设置用户初始头像
"""

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.utils import timezone

from authorize.models import User
from utils import auth
from utils.response import ReturnCode, CommonResponseMixin, wrap_json_response
from backend import settings

import json
import random

# Create your views here.


class AuthorizedView(View, CommonResponseMixin):

    def post(self, request):
        """
        授权登陆函数，方法为POST
        :param request: 传入的web请求，方法为POST，传入三个参数，code, appid
        :return: Jsonresponse data中储存状态码，表示登陆是否成功
        """
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        code = post_data.get('code')
        app_id = post_data.get('appid')

        if not code or not app_id:
            response = AuthorizedView.wrap_json_response(code=ReturnCode.BROKEN_PARAMS)
            return JsonResponse(data=response, safe=False)

        data = auth.c2s(app_id, code)
        open_id = data.get('openid')
        error_code = data.get('errcode')

        if error_code == -1:
            response = AuthorizedView.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)
        elif error_code == 40029:
            response = AuthorizedView.wrap_json_response(code=ReturnCode.WRONG_CODE)
            return JsonResponse(data=response, safe=False)
        elif error_code == 45011:
            response = AuthorizedView.wrap_json_response(code=ReturnCode.FREQUENCY_LIMITED)
            return JsonResponse(data=response, safe=False)

        request.session['open_id'] = open_id
        request.session['is_authorized'] = True
        nickname = settings.nickname + open_id[:-6]

        # 如果数据库中不存在该用户，则将其注册，存入数据库
        if not User.objects.filter(open_id=open_id):
            new_user = User(open_id=open_id, nickname=nickname)
            new_user.save()

        response = AuthorizedView.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)

    @auth.login_required
    def get(self, request):
        """
        获取用户信息
        :param request:
        :return: JsonResponse
        """
        open_id = request.session.get('open_id')
        user = User.objects.filter(open_id=open_id)
        data = dict()
        data['nickname'] = user.nickname
        data['phoneNumber'] = user.phone_number
        data['idNumber'] = user.id_number
        data['image'] = user.image
        response = wrap_json_response(data=data, code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


class LogoutView(View, CommonResponseMixin):

    @auth.login_required
    def post(self, request):
        """
        注销函数，方法为POST
        :param request: 传入的web请求
        :return: JsonResponse data储存状态码，表示是否注销成功
        """
        request.session.clear()
        response = LogoutView.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


class IDCertificationView(View, CommonResponseMixin):

    @auth.login_required
    def post(self, request):

        """
        实名认证方法
        :param request: 传入的web请求，需传入两个参数，身份证号 id_number 和姓名 name
        :return: JsonResponse data储存状态码，表示是否认证成功
        """

        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        name = post_data.get('name')
        id_number = post_data.get('idNumber')

        if not name or not id_number:
            response = IDCertificationView.wrap_json_response(code=ReturnCode.BROKEN_PARAMS)
            return JsonResponse(data=response, safe=False)

        data = auth.id_cert(name, id_number)
        data = json.loads(data)
        errcode = data.get('respCode')

        if errcode == '0002':
            response = IDCertificationView.wrap_json_response(code=ReturnCode.WRONG_NAME_FORM)
            return JsonResponse(data=response, safe=False)
        elif errcode == '0004':
            response = IDCertificationView.wrap_json_response(code=ReturnCode.WRONG_ID_FORM)
            return JsonResponse(data=response, safe=False)
        elif errcode == '0007':
            response = IDCertificationView.wrap_json_response(code=ReturnCode.NO_ID)
            return JsonResponse(data=response, safe=False)
        elif errcode == '0008':
            response = IDCertificationView.wrap_json_response(code=ReturnCode.MATCH_FAIL)
            return JsonResponse(data=response, safe=False)
        elif errcode == '0010':
            response = IDCertificationView.wrap_json_response(code=ReturnCode.FAILED)
            return JsonResponse(data=response, safe=False)

        open_id = request.session.get('open_id')
        user = User.objects.filter(open_id=open_id)
        user.name = name
        user.id_number = id_number
        user.save()

        response = LogoutView.wrap_json_response(code=ReturnCode.SUCCESS, message='success')
        return JsonResponse(data=response, safe=False)


class ImageView(View, CommonResponseMixin):

    @auth.login_required
    def post(self, request):
        """
        更改用户头像
        :param request: web请求，需传入一个参数，为用户更改的头像
        :return: JsonResponse data保存状态码
        """
        open_id = request.session.get('open_id')
        user = User.objects.filter(open_id=open_id)
        user.image = request.FILES['img']
        user.save()
        response = ImageView.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)


class PhoneCertificationView(View, CommonResponseMixin):

    @auth.login_required
    def get(self, request):
        """
        获取短信验证码
        :param request: web请求，phoneNumber 用户手机号
        :return: JsonResponse data储存状态码，短信是否发送成功
        """
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        phone_number = post_data.get('phoneNumber')

        if not phone_number:
            response = PhoneCertificationView.wrap_json_response(code=ReturnCode.BROKEN_PARAMS)
            return JsonResponse(data=response, safe=False)

        captcha = random.randint(10000, 100000 - 1)
        data = auth.phone_cert(phone_number, captcha)
        data = json.loads(data)
        if data.get('result') == -119:
            response = wrap_json_response(code=ReturnCode.WRONG_PHONE_NUMBER)
            return JsonResponse(data=response, safe=False)
        request.session['captcha'] = str(captcha)
        request.session['captcha_time'] = timezone.now()
        request.session['phone_number'] = phone_number

        response = PhoneCertificationView.wrap_json_response(code=ReturnCode.SUCCESS, message="success")
        return JsonResponse(data=response, safe=False)

    @auth.login_required
    def post(self, request):
        """
        验证码的验证
        :param request: web请求，captcha 用户填写的验证码
        :return:
        """
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)

        now = timezone.now()

        # 获取并删除有关session
        try:
            captcha_time = request.session.get('captcha_time')
            captcha_correct = request.session.get('captcha')
            del request.session['captcha_time']
            del request.session['captcha']
            del request.session['phone_number']
        except Exception:
            response = PhoneCertificationView.wrap_json_response(code=ReturnCode.WRONG_CAPTCHA)
            return JsonResponse(data=response, safe=False)

        captcha_user = post_data.get('captcha')
        phone_number = request.session.get('phone_number')

        if not captcha_user:
            response = PhoneCertificationView.wrap_json_response(code=ReturnCode.WRONG_CAPTCHA)
            return JsonResponse(data=response, safe=False)

        # 判定验证码过期
        delta = now - captcha_time
        if delta.seconds > 900:
            response = wrap_json_response(code=ReturnCode.CAPTCHA_DUE)
            return JsonResponse(data=response, safe=False)

        if captcha_correct == captcha_user:
            open_id = request.session.get['open_id']
            user = User.objects.filter(open_id=open_id)
            user.phone_number = phone_number
            user.save()
            response = wrap_json_response(code=ReturnCode.SUCCESS)
            return JsonResponse(data=response, safe=False)
        else:
            response = wrap_json_response(code=ReturnCode.CAPTCHA_DUE)
            return JsonResponse(data=response, safe=False)


class NickNameView(View, CommonResponseMixin):

    @auth.login_required
    def post(self, request):
        """
        更改用户昵称
        :param request: nickname 新的昵称
        :return: JsonResponse
        """
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)
        nickname = post_data.get('nickname')
        open_id = request.session.get('open_id')
        user = User.objects.filter(open_id=open_id)
        user.nickname = nickname
        response = NickNameView.wrap_json_response(code=ReturnCode.SUCCESS)
        return JsonResponse(data=response, safe=False)
