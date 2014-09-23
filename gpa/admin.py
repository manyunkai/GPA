# -*-coding:utf-8 -*-
"""
Created on 2014-09-13

@author: Danny
DannyWork Project
"""

from django.contrib import admin
from django.db import models

from gpa.forms import GPARuleFormForTypeF, GPARuleFormForTypeS
from gpa.models import Course, GPARule, Point, Segment, calc_point


def point_display(rule):
    def get_point_display(obj):
        p = Point.objects.get(rule=rule, course=obj)
        return u'{0} / {1}'.format(p.score, p.score_with_credit)

    get_point_display.short_description = rule.name
    return get_point_display


class SegmentInline(admin.TabularInline):
    model = Segment


class GPARuleAdmin(admin.ModelAdmin):
    form = GPARuleFormForTypeS
    inlines = [SegmentInline]

    change_list_template = 'admin/gpa/gpa_rule_change_list.html'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
            obj.type = 'F' if request.GET.get('type', 'F') == 'F' else 'S'
        obj.save()

        self.rule = obj

    def queryset(self, request):
        qs = super(GPARuleAdmin, self).queryset(request)
        return qs.filter(user=request.user)

    def save_change_to_courses(self):
        for course in Course.objects.all():
            calc_point(course, self.rule)

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.type == 'F' or request.GET.get('type') == 'F':
            self.form = GPARuleFormForTypeF
            self.inlines = []
        else:
            self.form = GPARuleFormForTypeS
            self.inlines = [SegmentInline]
        return super(GPARuleAdmin, self).get_form(request, obj, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        res = super(GPARuleAdmin, self).add_view(request, form_url, extra_context)
        if request.method == 'POST' and getattr(self, 'rule', None):
            self.save_change_to_courses()
        return res

    def change_view(self, request, object_id, form_url='', extra_context=None):
        res = super(GPARuleAdmin, self).change_view(request, object_id, form_url, extra_context)
        if request.method == 'POST':
            self.save_change_to_courses()
        return res


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'no', 'sn', 'credit', 'score']
    change_list_template = 'admin/gpa/gpa_course_change_list.html'
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.save()

    def queryset(self, request):
        qs = super(CourseAdmin, self).queryset(request)
        return qs.filter(user=request.user)

    def get_list_display(self, request):
        list_display = list(self.list_display)
        for rule in GPARule.objects.filter(user=request.user):
            column_name = 'rule_{0}'.format(rule.id)
            list_display.append(column_name)
            setattr(self, column_name, point_display(rule))
        return list_display

    def changelist_view(self, request, extra_context=None):
        courses = self.queryset(request)
        avas = []
        total_credit = courses.aggregate(total_credit=models.Sum('credit')).get('total_credit')
        for rule in GPARule.objects.filter(user=request.user):
            total_score = Point.objects.filter(rule=rule, course__in=courses).aggregate(total_score=models.Sum('score_with_credit')).get('total_score')
            try:
                gpa_avag = round(total_score / total_credit, 6)
            except Exception, e:
                gpa_avag = 0
            avas.append([rule.name, gpa_avag])

        return super(CourseAdmin, self).changelist_view(request, {'avas': avas})


admin.site.register(GPARule, GPARuleAdmin)
admin.site.register(Course, CourseAdmin)