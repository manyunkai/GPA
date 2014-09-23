GPA
===

A Simple GPA Tool, developed in Django. 

一个简易的课程成绩录入与GPA计算工具。能自定义GPA算法，快速录入成绩并在一个页面中综合查看所有课程成绩、各绩点与平均绩点。

Environment（环境）
---

* Django == 1.5.5
* django-grappelli == 2.4.8
* sympy == 0.7.5

Issues（问题）
---

在进行公式计算时直接调用了eval将字符串中的公式转为Python语句，这是不安全的做法。
