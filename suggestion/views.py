"""
@author 彭奥
@cooperation 绿萌

意见反馈功能模块
"""

from django.views import View
from django.http import JsonResponse

from .models import Suggestion
from authorize.models import User
from utils.response import CommonResponseMixin, ReturnCode
from utils.auth import login_required

import json
# Create your views here.


class SuggestionView(View, CommonResponseMixin):

    """
    意见反馈视图函数
    """
    @login_required
    def post(self, request):
        """
        获取意见并将意见发送至邮箱中
        :param request: web请求，需要两个参数，type 表示建议种类"建议"，"吐槽"，"其他"，content为建议内容
        :return: JsonResponse data储存状态码
        """
        post_data = request.body.decode('utf-8')
        post_data = json.loads(post_data)

        content = post_data.get("content")
        s_type = post_data.get("type")
        open_id = request.session.get('open_id')

        if type != 0 and type != 1 and type != 2:
            response = SuggestionView.wrap_json_response(code=ReturnCode.FAILED, message='param type error')
            return JsonResponse(data=response, safe=False)

        user = User.objects.filter(open_id=open_id)
        suggestion = Suggestion(content=content, s_type=s_type, user=user)
        suggestion.save()

        response = SuggestionView.wrap_json_response(code=ReturnCode.SUCCESS, message='success')
        return JsonResponse(data=response, safe=False)
