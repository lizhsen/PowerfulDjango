# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_citys = CityDict.objects.all()
        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        # 取出筛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        # 排序功能
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs, per_page=3, request=request)
        orgs = p.page(page)
        org_nums = all_orgs.count()
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        user_ask_form = UserAskForm(request.POST)
        print(user_ask_form.fields)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg": "添加错误"}', content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        current_page = "course"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    """
    机构介绍页
    """

    def get(self, request, org_id):
        current_page = "desc"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """

    def get(self, request, org_id):
        current_page = "teacher"
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(org_id), fav_type=2):
                has_fav = True
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'current_page': current_page,
            'all_teacher': all_teacher,
            'has_fav': has_fav
        })


class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg": "用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果已收藏再次点击代表取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg": "收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"success", "msg": "收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        # 对讲师进行排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by("-click_nums")
        # 热门讲师推荐
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_teachers, per_page=3, request=request)
        teachers = p.page(page)
        teacher_nums = all_teachers.count()
        return render(request, 'teachers-list.html', {
            'all_teachers': teachers,
            'teacher_nums': teacher_nums,
            'sorted_teachers': sorted_teachers,
            'sort': sort
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher_courses = Course.objects.filter(teacher=teacher)
        sorted_teachers = Teacher.objects.all().order_by("-click_nums")[:3]
        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            'sorted_teachers': sorted_teachers,
            'teacher_courses': teacher_courses,
            'has_fav_teacher': has_fav_teacher,
            'has_fav_org': has_fav_org,

        })
