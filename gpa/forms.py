# -*-coding:utf-8 -*-
"""
Created on 2014-09-13

@author: Danny
DannyWork Project
"""

from django import forms

from gpa.models import GPARule


class GPARuleFormForTypeF(forms.ModelForm):
    FORMULA_ALLOWED_ITEMS = set([' ', '%', '+', '*', '-', '/', '.', 'x',
                                 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'])

    def clean_formula(self):
        f = self.cleaned_data.get('formula', '')
        if not set(f).issubset(self.FORMULA_ALLOWED_ITEMS):
            raise forms.ValidationError(u'非法的公式，仅允许包含“空格”、“+”、“-”、“*”、“/”、“%”和“数字”。')
        return f

    class Meta:
        model = GPARule
        fields = ['name', 'formula', 'precision']


class GPARuleFormForTypeS(forms.ModelForm):

    class Meta:
        model = GPARule
        fields = ['name']
