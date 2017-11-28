#encoding=utf8
__author__ = 'kingkk'
__date__ = '2017/11/9 19:45'

from django.conf.urls import url,include

from views import *

urlpatterns = [
    #课程列表页
    url(r'^list/$', CourseListView.as_view() ,name="course_list"),
    #课程详情页
    url(r'^detail/(?P<course_id>.*)/$', CourseDetailView.as_view(), name="course_detail"),
    #课程信息页
    url(r'^info/(?P<course_id>.*)/$', CourseInfoView.as_view(), name="course_info"),
    # 课程评论页
    url(r'^comment/(?P<course_id>.*)/$', CommentsView.as_view(), name="course_comments"),
    # 添加课程评论
    url(r'^add_comment$', AddCommentsView.as_view(), name="add_comment"),
    #视频播放页
    url(r'^video/(?P<video_id>.*)/$', VideoPlayView.as_view(), name="video_play"),
]