"""
@author 彭奥
建议相关数据库
"""

from django.db import models

from authorize.models import User

# Create your models here.

# 建议类型选项
TYPE_CHOICE = ((0, '建议'),
               (1, '吐槽'),
               (2, '其他'))


class Suggestion(models.Model):
    """
    content 储存建议内容
    user 储存提出建议的用户信息
    type 提出建议的种类
    """
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    s_type = models.IntegerField(choices=TYPE_CHOICE)

