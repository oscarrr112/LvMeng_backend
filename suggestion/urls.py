# -*- coding: utf-8 -*-
# @Time    : 2019-08-13 20:04
# @Author  : 彭奥
# @Cooperation: LvMeng
# @Site    : 
# @File    : urls.py
# @Software: PyCharm

from django.urls import path

from suggestion import views

urlpatterns = [
    path('suggest', views.SuggestionView.as_view())
]
