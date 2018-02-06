# -*- coding: utf-8 -*-

import xadmin

from .models import EmailVerifyRecord, Banner, UserProfile


class EmailVerifyRecordAdmin(object):
    list_display = ["code", "email", "send_type"]
    search_fields = ["code", "email", "send_type"]
    list_filter = ["code", "email", "send_type"]





class BannerAdmin(object):
    list_display = ["title", "image", "url", "index", "add_time"]
    search_fields = ["title", "image", "url", "index"]
    list_filter = ["title", "image", "url", "index", "add_time"]


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

