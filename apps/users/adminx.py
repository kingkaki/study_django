#encoding=utf8

import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = False

class GlobalSettings(object):
    site_title =  "慕学后台管理系统"
    site_footer = "慕学在线网"
    menu_style = "accordion"

class EmailVerifyRecordAdmin(object):
    model_icon = 'fa fa-address-book-o'
    list_display = ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type'] #无法对时间进行search，否则会报错
    list_filter = ['code','email','send_type','send_time']

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']



xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)