# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
# Create your views here.


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        sort = request.GET.get("sort", "")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]
        if sort:
            if sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
            elif sort == "students":
                all_courses = all_courses.order_by("-students")
        # 对课程列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_courses, per_page=3, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    """
    课程信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        tag = course.tag
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        if tag:
            related_courses = Course.objects.filter(tag=tag)[:2]
        else:
            related_courses = []
        return render(request, 'course-detail.html', {
            'course': course,
            'related_courses': related_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses1 = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses1:
            user_courses1 = UserCourse(user=request.user, course=course)
            user_courses1.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        user_courses1 = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses1:
            user_courses1 = UserCourse(user=request.user, course=course)
            user_courses1.save()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course.id for user_course in all_user_courses]
        related_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]
        course_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': course_resources,
            'all_comments': all_comments,
            'related_courses': related_courses,
        })


class AddCourseCommentView(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.user = request.user
            course_comments.comments = comments
            course_comments.save()
            return HttpResponse('{"status":"success", "msg": "评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success", "msg": "添加失败"}', content_type='application/json')




