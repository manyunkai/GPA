GPA
===

A Simple GPA Tool, developed in Django. 

一个简易的课程成绩录入与 GPA 计算工具。能自定义 GPA 算法，快速录入成绩并在一个页面中综合查看所有课程成绩、各绩点与平均绩点。

环境
---

* Django == 1.5.5
* django-grappelli == 2.4.8
* sympy == 0.7.5

问题
---

在进行公式计算时直接调用了 eval 将字符串中的公式转为 Python 语句，这是不安全的做法。

运行这个工程
---

运行前，请检查当前包环境。然后建立 settings/__init__.py 文件，导入 settings/base.py 中的配置，并自定义数据库配置。
