from django.urls import path
from . import views
from django.contrib.auth.views  import   LogoutView


app_name = "core"

urlpatterns = [
    # func
    path("change_lang/", views.change_lang,                                                 name="change_lang"     ),
    # auth
    path("signup/",      views.signup,                                                      name="signup"          ),
    path("login/",       views.LoginViewSec.as_view(template_name="pages/login.html"),      name="login"           ),
    path("signup/<str:lang>/", views.signup,                                                name="signup"          ),
    path("login/<str:lang>/",  views.LoginViewSec.as_view(template_name="pages/login.html"),name="login"           ),
    path("logout/", LogoutView.as_view(),                                                   name="logout"          ),
    # landing
    path("", views.landing      ,                                                           name="landing"         ),
    path("welcome/<str:lang>/", views.landing      ,                                        name="landing"         ),
    # courses
        # Workshops

    
    # payment
    path("payment/<str:lang>/", views.payment, name="payment"),

    path("payment/", views.payment, name="payment"),
    path("meetups/<str:lang>/", views.meetup, name="meetups"),
    path("meetups/", views.meetup, name="meetups"),
    path("meetups/<str:lang>/<int:pk>/", views.meetup_detail, name="meetup"),
    path("meetups/<str:lang>/", views.meetup_detail, name="meetup"),



    path("send_test_email/", views.send_test_email, name="send_test_email"),


    path("summits/<str:lang>/", views.summit, name="summit"),
    path("summits/", views.summit, name="summit"),
    path("summits/<str:lang>/<int:pk>/", views.summit_detail, name="summit_detail"),
    path("summits/<str:lang>/", views.summit_detail, name="summit_detail"),

    path("speakers/<str:lang>/<int:pk>/", views.speaker, name="speaker"),
    path("speakers/<str:lang>/", views.speaker, name="speaker"),
    path("speakers/", views.speaker, name="speaker"),


    path("check_qr_valid_or_not/<str:uuid>/", views.check_qr_valid_or_not, name="check_qr_valid_or_not"),
    path("check_qr_valid_or_not/", views.check_qr_valid_or_not, name="check_qr_valid_or_not"),

]

