from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from core.models import models
# Create your views here.

def courses_categories_list(req:HttpRequest, lang=None) ->HttpResponse:


    if  lang == None:
        
        return redirect(
            reverse("core:couese_list_view", args=["en"])
        )
    data = []
    categories = models.CourseCategory.objects.all()
    courses    = models.Courses.objects.all()
    for i in categories:
        data.append(
            {
            "name_en"   : i.name_en,
            "name_ar"   : i.name_ar,
            "courses"   : courses.filter(category=i)
        }
        )
    context = {
        "lang"    : lang     ,
        "active"  : "courses",
        "data" : data
    }

    return render(req, "pages/courses.html", context)



def course_list_view(req:HttpRequest, lang=None, course=None):


    if  lang == None:
        
        return redirect(
            reverse("core:couese_list_view", args=["en"])
        )
    
    categories = models.CourseCategory.objects.all() 
    if course is None:
        courses    = models.Courses.objects.all()
    else:
        courses    = models.Courses.objects.filter(category=models.CourseCategory.objects.get(name_en=course))

    context = {
        "lang"          : lang      ,
        "active"        : "courses" ,
        "courses"       : courses   ,


    }
    return render(req, "pages/courses.html", context)



# course details

def course_detail(req:HttpRequest, lang=None, pk:int=None) -> HttpResponse:

    if pk == None:
        return redirect(
            reverse("core:couese_list_view", args=["en"])

        )
    if  lang == None:
        return redirect(
            reverse("core:course_detail", args=["en", pk])
        )
    
    the_course = models.Courses.objects.get(pk=pk)
    if req.user.is_authenticated:

        usercourses = models.UserCourses.objects.filter(user=req.user, course=the_course)
        if usercourses.count() == 0:
            have_the_couerse = False
        else:   
            have_the_couerse = True
    else:
        have_the_couerse = False
    context = {
        "lang"     : lang       ,
        "active"   : "courses"  ,
        "course"   : the_course ,
        "aviable"  : have_the_couerse,
    }
    
    return  render(req, "pages/course_detail.html", context=context)





def instructor_detail(req:HttpRequest, lang=None, pk:int=None) -> HttpResponse:
    
    if pk == None:
        return redirect(
            reverse("core:courses_categories", args=["en"])
        )
    if  lang == None:
        return redirect(
            reverse("core:instructor_detail", args=["en", pk])
        )
    
    instructor  = models.Instructor.objects.get(pk=pk)
    instructor_courses = models.Courses.objects.filter(instructor=instructor)

    context = {
        "lang"     : lang       ,
        "active"   : "courses"  ,
        "instructor"   : instructor ,
        "courses" : instructor_courses
    }
    
    return  render(req, "pages/instructor_detail.html", context=context)

def video_detail(req:HttpRequest, lang=None, course=None, pk:int=None) -> HttpResponse:
    
    the_course = models.Courses.objects.get(pk=course)
    the_videos  = models.Ep.objects.filter(course=the_course)

    if pk == None:

        context = {
            "lang"     : lang       ,
            "active"   : "courses"  ,
            "course"   : the_course ,
            "videos"    : the_videos  ,
        }
        return  render(req, "pages/video_detail.html", context=context)
    if  lang == None:
        return redirect(
            reverse("core:video_detail", args=["en", course, pk])
        )
    
    the_video  = models.Ep.objects.get(pk=pk)
    the_videos = the_videos.exclude(pk=pk)
    context = {
        "lang"     : lang       ,
        "active"   : "courses"  ,
        "course"   : the_course ,
        "video"    : the_video  ,
        "others"   : the_videos  ,
    }
    return  render(req, "pages/watch_video.html", context=context)

