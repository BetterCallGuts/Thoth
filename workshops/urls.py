from django.urls import path
from . import views

app_name = "workshops"
urlpatterns = [
    path("workshop/<str:lang>/", views.work_shop, name="workshop"),
    
]
