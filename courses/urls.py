from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("courses/<str:lang>/", views.courses_categories_list, name="courses_categories"),
    path("courses/", views.courses_categories_list, name="courses_categories"),
    #
    #course detailes 
    path("courses/<str:lang>/<int:pk>/", views.course_detail, name="course_detail"),
    # video details

    path("courses/<str:lang>/<str:course>/ep/", views.video_detail,                        name="video_detail"),
    path("courses/<str:lang>/<str:course>/ep/<int:pk>/", views.video_detail,                        name="video_detail"),

    path("courses/<str:lang>/<str:course>/", views.course_list_view,                        name="couese_list_view"),
    path("instructor/<str:lang>/<int:pk>/", views.instructor_detail, name="instructor_detail"),
    path("instructor/<str:lang>/", views.instructor_detail, name="instructor_detail"),
    path("instructor/", views.instructor_detail, name="instructor_detail"),

]
