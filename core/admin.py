from typing import Any, Iterable
from django.contrib import admin

from django.http import HttpRequest
from typing import Type,  Any
from .models import models
from .models.workshops import WorkShopsCategory
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .views import send_them_email


admin.site.unregister(User,   )




admin.site.site_header= "Thoth"
admin.site.site_title = "Thoth"
admin.site.index_title = "Thoth"
admin.site.site_url = "https://thoth.net"
# ----------- inline stacks
class VideoInlineStack(admin.StackedInline):
    
    model = models.Ep
    extra = 0
    verbose_name = "حلقة"
    verbose_name_plural = "حلقات"

class qrcodeSummitTicketInlineStack(admin.StackedInline):
    model = models.QrcodeForTicket
    extra = 0
    verbose_name = "SummitTicket"
    verbose_name_plural = "SummitTickets"
    fields = ("show_image", "chose_message", "send_mail")
    readonly_fields = ("show_image", "chose_message", "send_mail")

# 
class UserCoursesInlineStack(admin.StackedInline):
    model = models.UserCourses
    extra = 0
    verbose_name = " course"
    verbose_name_plural = "user courses"

#------------Instructor


#------------ AdminModels

class CoursesAdminStyle(admin.ModelAdmin):
    list_display = ["more", "instructor", "name_ar", "name_en","show_image",  "category"]
    list_display_links = ["more"]
    inlines      = [
        VideoInlineStack,
    ]
    list_filter = ("instructor", "category")



    search_fields = ["name_ar", "name_en", "instructor__name_ar", "instructor__name_en"]




class InstructorAdminStyle(admin.ModelAdmin):
    
    list_display = ["more" , "name_ar", "name_en", "show_image", "time_added"]
    list_display_links = ("more",)


class CourseTypeAdminStyle(admin.ModelAdmin):

    list_display = ["more" , "name_ar", "name_en"]
    list_display_links = ("more", )



class MeetupAdminStyle(admin.ModelAdmin):
    pass


class MeetupTicketAdminStyle(admin.ModelAdmin):
    pass




class UserCoursesAdminStyle(UserAdmin):

    def get_inlines(self, request: HttpRequest, obj: Any | None) ->  Iterable[Type[admin.options.InlineModelAdmin]]:
        inlines = super().get_inlines(request, obj)
        return inlines + ( UserCoursesInlineStack  ,)


class WorkShopsCategoryAdminStyle(admin.ModelAdmin):
    list_display = ["more", "name_ar", "name_en"]
    list_display_links = ("more", )
    search_fields = ["name_ar", "name_en"]

class SummitAdminStyle(admin.ModelAdmin):
    list_display = ["more", "name_ar", "name_en",  ]
    list_display_links = ("more",)
    search_fields = ["name_ar", "name_en"]


class SummitTicketAdminStyle(admin.ModelAdmin):
    list_display = ["more", "user", "summit", "is_used","name", "email", "phone_number", "job_title"]
    list_display_links = ("more",)
    search_fields = ["name",  "summit__name_ar", "summit__name_en", "email", "phone_number", "job_title"]
    inlines      = [
        qrcodeSummitTicketInlineStack,
    ]
    list_filter = ["is_used", "did_he_pay" 
                , "summit", "sended_mail", 
                "ticket_type"]
    actions = [
        "reset_payment_and_used_tickets_and_send_email",
        "send_email",
    ]

    def reset_payment_and_used_tickets_and_send_email(self, request, queryset):
        queryset.update(did_he_pay=False, is_used=False, sended_mail=False)
        self.message_user(request, f"Tickets reseted")

    def send_email(self, request, queryset):
        
       

        send_them_email(request, queryset)


class SpeakersAdminStyle(admin.ModelAdmin):
    list_display = ["more", "name_ar", "name_en",  ]
    list_display_links = ("more",)
    search_fields = ["name_ar", "name_en"]



admin.site.register(models.Instructor     , InstructorAdminStyle  )
admin.site.register(models.Courses        , CoursesAdminStyle     )  
admin.site.register(models.CourseCategory , CourseTypeAdminStyle  )
admin.site.register(models.Meetup         , MeetupAdminStyle      )
admin.site.register(models.MeetupTicket   , MeetupTicketAdminStyle)
admin.site.register(WorkShopsCategory, WorkShopsCategoryAdminStyle)
admin.site.register(User, UserCoursesAdminStyle)
admin.site.register(models.Summit, SummitAdminStyle)
admin.site.register(models.SummitTicket, SummitTicketAdminStyle)

admin.site.register(models.Speakers, SpeakersAdminStyle)    

admin.site.register(models.Messages, )