# -*-coding:utf-8 -*-
"""
Created on 2014-09-13

@author: Danny
DannyWork Project
"""

from sympy import Symbol

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class GPARule(models.Model):
    TYPE_CHOICES = (
        ('F', '计算公式'),
        ('S', '分段取值')
    )

    user = models.ForeignKey(User, verbose_name=u'用户')
    name = models.CharField(u'名称', max_length=64)
    type = models.CharField(u'模式', max_length=1, choices=TYPE_CHOICES)
    formula = models.CharField(u'公式', max_length=256, blank=True)
    precision = models.IntegerField(u'精度', default=2)

    class Meta:
        verbose_name = u'GPA算法'
        verbose_name_plural = u'GPA算法'

    def __unicode__(self):
        return self.name


class Segment(models.Model):
    rule = models.ForeignKey(GPARule, verbose_name=u'GPA算法')
    high = models.IntegerField(u'高分')
    low = models.IntegerField(u'低分')
    gpa = models.FloatField(u'绩点')

    class Meta:
        verbose_name = u'取值段'
        verbose_name_plural = u'取值段'

    def __unicode__(self):
        return u'分数段（>={0}）'.format(self.low)


class Course(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    name = models.CharField(u'课程名', max_length=64)
    no = models.CharField(u'课程号', max_length=16, blank=True)
    sn = models.CharField(u'序号', max_length=16, blank=True)
    credit = models.FloatField(u'学分')
    score = models.FloatField(u'成绩')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = u'课程'

    def __unicode__(self):
        return self.name


class Point(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    rule = models.ForeignKey(GPARule, verbose_name=u'GPA算法')
    score = models.FloatField(u'绩点')
    score_with_credit = models.FloatField(u'绩点x学分')

    class Meta:
        verbose_name = u'绩点计算结果'
        verbose_name_plural = u'绩点计算结果'

    def __unicode__(self):
        return u'{0} - {1}'.format(self.course, self.rule)


def calc_point(course, rule):
    try:
        point = Point.objects.get(course=course, rule=rule)
    except Point.DoesNotExist:
        point = Point()
        point.course = course
        point.rule = rule

    if rule.type == 'F':
        x = Symbol('x')
        try:
            s = eval(rule.formula)
        except Exception, e:
            g = 0
        else:
            g = round(s.subs(x, course.score), rule.precision)
    else:
        s = rule.segment_set.filter(low__lte=course.score).order_by('-low')
        g = s[0].gpa if s.exists() else 0

    point.score = g
    point.score_with_credit = g * course.credit
    point.save()


def course_post_save(**kwargs):
    course = kwargs.get('instance')
    for rule in GPARule.objects.all():
        calc_point(course, rule)


post_save.connect(course_post_save, sender=Course)
