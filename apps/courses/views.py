#encoding=utf8
from django.shortcuts import render
from django.views.generic.base import View
from django.http import  HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from models import Course,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        #课程搜索
        search_keywords = request.GET.get("keywords","")
        if search_keywords:
            all_courses = all_courses.filter(Q(name__contains=search_keywords)|Q(desc__contains=search_keywords)|Q(detail__contains=search_keywords))

        #课程排序
        sort = request.GET.get('sort','')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by('-students')
            elif sort == "hot":
                all_courses = all_courses.order_by('-click_nums')

        #做分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    """
    课程详情页
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums+=1
        course.save()

        tag=course.tag
        if tag:
           relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses =[]

        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated() and UserFavorite.objects.filter(user = request.user,fav_id=course.id,fav_type=1):
            has_fav_course = True

        if request.user.is_authenticated() and UserFavorite.objects.filter(user = request.user,fav_id=course.course_org.id,fav_type=2):
            has_fav_org = True

        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org,
        })


class CourseInfoView(LoginRequiredMixin,View):
    """
    课程章节信息
    """
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students+=1
        course.save()
        # #查询用户是否已经开始学习该课程
        has_study = UserCourse.objects.filter(user=request.user,course=course)
        if not has_study:
            has_study = UserCourse(user=request.user,course=course)
            has_study.save()

        #获取相同课程的数据
        user_courses = UserCourse.objects.filter(course=course)
        #获取每条数据中用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出用户组的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程ID
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        #获取学过该用户课程的课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by("-click_nums")[:3]

        return render(request,'course-video.html',{
            'course':course,
            'relate_courses':relate_courses,
        })


class CommentsView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_comments = CourseComments.objects.all()

        #获取相同课程的数据
        user_courses = UserCourse.objects.filter(course=course)
        #获取每条数据中用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出用户组的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程ID
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        #获取学过该用户课程的课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by("-click_nums")[:3]
        return render(request, 'course-comment.html', {
            'course': course,
            'all_comments':all_comments,
            'relate_courses': relate_courses,
        })


class AddCommentsView(View):
    """
    用户添加课程评论
    """
    def post(self, request):
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get("course_id","")
        comments = request.POST.get("comments","")
        if course_id>0 and comments:
            course_comments = CourseComments()
            course_comments.course = Course.objects.get(id=int(course_id))
            course_comments.user = request.user
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type="application/json")



class VideoPlayView(View):
    """
    视频播放页面
    """
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        # #查询用户是否已经开始学习该课程
        has_study = UserCourse.objects.filter(user=request.user,course=course)
        if not has_study:
            has_study = UserCourse(user=request.user,course=course)
            has_study.save()

        #获取相同课程的数据
        user_courses = UserCourse.objects.filter(course=course)
        #获取每条数据中用户的id
        user_ids = [user_course.user.id for user_course in user_courses]
        #取出用户组的课程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        #取出所有课程ID
        course_ids = [all_user_course.id for all_user_course in all_user_courses]
        #获取学过该用户课程的课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by("-click_nums")[:3]

        return render(request,'course-play.html',{
            'course':course,
            'relate_courses':relate_courses,
            'video':video,
        })