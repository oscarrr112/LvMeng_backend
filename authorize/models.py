"""
@author 彭奥

建立用户数据表
"""

from django.db import models

# Create your models here.


class User(models.Model):

    """
    用户表
    """

    """
    open_id 用户的微信open_id
    nickname 用户在绿萌的昵称
    phone_number 用户的电话号码
    name 用户的真实姓名
    id_number 用户的身份证号
    image 用户头像
    """

    open_id = models.CharField(max_length=32, unique=True)
    nickname = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=256)
    id_number = models.CharField(max_length=20)
    image = models.ImageField()

    class Meta:
        """
        设置表的排序方式为按照open_id升序排序
        """
        ordering = ['open_id']
        indexes = [
            models.Index(fields=['open_id'])
        ]
