from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from core.models import models, workshops



def work_shop(req:HttpRequest , lang=None) ->HttpResponse:

    if  lang == None:
        
        return redirect(
            reverse("core:workshop", args=["en"])
        )
    
    
    WorkShopsCategory = workshops.WorkShopsCategory.objects.all()
    
    context = {
        "lang" : lang         ,
        "active" : "workshops",
        "data" : WorkShopsCategory


    }


    return render(req, "pages/workshops/landing.html", context)
