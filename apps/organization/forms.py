# -*- coding: utf-8 -*-
import re
from django import forms

from operation.models import UserAsk


class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ["name", "mobile", "course_name"]

    # 必须以clean开头
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        p = re.compile('^1[358]\d{9}$|^147\d{8}$|^176\d{8}')
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code='mobile_invalid')
