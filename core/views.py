from typing import Any
from django.shortcuts import render, redirect
from django.http      import HttpRequest, HttpResponse
from .form            import UserCustomForm, SummitForm
from django.urls      import reverse
from django.contrib.auth.views  import  LoginView
from .models                    import models
from random                     import choice
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.utils.html import mark_safe, strip_tags
from django.contrib.messages import success ,error
from django.template.loader import render_to_string
from django_xhtml2pdf.utils import generate_pdf
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.db.models.query import QuerySet
import os
import time

# Landing Page Request Handle Function
def landing(req:HttpRequest, lang=None) -> HttpResponse:
    
    if  lang == None:
        return redirect(
            reverse("core:landing", args=["en"])
        )
    context = {

        "lang"     : lang,
        "active"   : "home"

    }
    c = choice([True, False])

    if c :

        return  render(req, "pages/landing1.html", context=context)
    
    return  render(req, "pages/landing2.html", context=context)




def signup(req:HttpRequest, lang=None) -> HttpResponse:

    if  lang == None:
        return redirect(
            reverse("core:signup", args=["en"])
        )

    if req.method == "POST":
        form = UserCustomForm(req.POST)

        if form.is_valid():
            form.save()

            return redirect(reverse("core:login"))

    form = UserCustomForm()

    context = {
        "form" : form,
        "lang" : lang
    }
    
    return  render(req, "pages/signup.html", context)


class LoginViewSec(LoginView):
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        x = super().get_context_data(**kwargs)
        x['lang'] = self.kwargs.get("lang", None)
        if  x['lang'] == None:
            return redirect(reverse("core:login", args=["en"]))

        return x
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        
        x = self.kwargs.get("lang", None)
        if  x == None:
            return redirect(
                reverse("core:login", args=["en"])
            )
        
        return super().render_to_response(context, **response_kwargs)
    
def change_lang(req:HttpRequest):
    
    url:str = req.META['HTTP_REFERER']
    
    if "en" in url:
        url = url.replace("en", "ar")
    elif "ar" in url:
        url = url.replace("ar", "en")

    return redirect(url)







def payment(req: HttpRequest, lang=None) -> HttpResponse :

    if lang == None:

        return redirect(reverse("payment", args=["en"]))

    context = {
        "lang" : lang         ,
    }
    return render(req, "pages/payment.html", context)






# instructor_detail.html





def meetup(req:HttpRequest, lang=None) -> HttpResponse:
    
    if  lang == None:
        
        return redirect(
            reverse("core:meetup", args=["en"])
        )
    
    meetups = models.Meetup.objects.all()
    context = {
        "lang" : lang         ,
        "active" : "meetups",
        "meetups" : meetups
    }
    return render(req, "pages/meetup.html", context)


def meetup_detail(req:HttpRequest, lang=None, pk:int=None) -> HttpResponse:
    
    if pk == None:
        return redirect(
            reverse("core:meetups", args=["en"])
        )
    if  lang == None:
        return redirect(
            reverse("core:meetup_detail", args=["en", pk])
        )
    
    meetup = models.Meetup.objects.get(pk=pk)
    meetups = meetups.exclude(pk=pk)
    context = {
        "lang"     : lang       ,
        "active"   : "meetups"  ,
        "meetup"   : meetup ,
        "others"   : meetups  ,
    }
    return  render(req, "pages/meetup_detail.html", context=context)

def render_to_pdf(template, context):
   template = get_template(template)
   html  = template.render(context)
   result = BytesIO()
   pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
   if not pdf.err:
       return HttpResponse(result.getvalue(), content_type='application/pdf')
   return None

# ###############################################################################
def send_them_email(request:HttpRequest, queryset:QuerySet[models.SummitTicket]):
    # msg = models.Messages.objects.first()
    counter = 0
    for obj in queryset:


      the_code = models.QrcodeForTicket.objects.get(summitticket=obj)

      context = {
        "url_my_image" : settings.SITE_DOMAIN + the_code.qrcode.url,
        # "msg" : msg,
        "his_name" : obj.name,
    }   
      
      subject =  f"Welcome to {obj.summit.name_en}"
      if obj.ticket_type == "S" or obj.ticket_type == None or obj.ticket_type != "V":
            context["ticket_type"] =  settings.SITE_DOMAIN +  "/static/image/standard_ticket.jpeg" 

            html_message = render_to_string('emails/summit_temp.html', context)
      elif obj.ticket_type == "V":
        context["ticket_type"] =  settings.SITE_DOMAIN +  "/static/image/Vip_ticket.jpeg"
        html_message = render_to_string('emails/summit_temp_vip.html', context)

      plaintext_message = strip_tags(html_message)
      from_email = settings.EMAIL_HOST_USER
      message = EmailMultiAlternatives(subject=subject , body=plaintext_message, from_email= from_email, to= [obj.email])  
      message.attach_alternative(html_message, "text/html")
      message.send() 
      counter += 1
      time.sleep(1)
      if counter == 10:
        time.sleep(10)
        counter = 0

def send_test_email(request:HttpRequest):
    # 
    the_message = request.GET.get('hiddenMessage')
    the_tiket = request.GET.get('pk')
    ticket_email = request.GET.get('hiddenEmail')
    print(the_tiket)
    qrcode = models.QrcodeForTicket.objects.get(pk=int(the_tiket))
    summitticket = models.SummitTicket.objects.filter(email=ticket_email)
    summitticket = summitticket[0]
    summitticket.sended_mail = True
    summitticket.save()
    message = models.Messages.objects.get(pk=int(the_message))
    message = mark_safe(message.Text)

    subject = f'Ticket for {summitticket.summit.name_en}'
    

    context = {
        "url_my_image" : settings.SITE_DOMAIN + qrcode.qrcode.url,
        "msg" : message
    }
    html_message = render_to_string('emails/summit_temp.html', context)
    # context["imgagin"] = True
    # pdf          = generate_pdf('emails/summit_temp.html', context=context)
    # path = os.path.join(r"F:\ticket.pdf")
    # with open(path, 'wb') as f:
    #     f.write(pdf.getbuffer().tobytes())

    # context["pdf"] = pdf
    # html_message = render_to_string('emails/summit_temp.html', context)
    # print(pdf.__sizeof__())
    # recipient_list = ['bettercallguts@gmail.com']
    from_email = settings.EMAIL_HOST_USER
    plaintext_message = strip_tags(html_message)
    message = EmailMultiAlternatives(subject=subject,body= plaintext_message, from_email= from_email, to= [ticket_email])  
    
    # message.attach('Ticket.pdf', pdf.read(), 'application/pdf')
    # message.attach_file(path)
    message.attach_alternative(html_message, "text/html")
    message.send()
    success(request, "Email sent successfully")

    # send_mail(subject,mark_safe( message), from_email, recipient_list, fail_silently=True)
    return redirect(request.META['HTTP_REFERER'])



def summit(req:HttpRequest, lang=None) -> HttpResponse:
    if req.method == "POST":
        temp = {}
        temp['csrfmiddlewaretoken'] =req.POST.get('csrfmiddlewaretoken')
        temp['summit'] = req.POST.get('summit_id')
        temp['name'] = req.POST.get('username')
        temp['email'] = req.POST.get('email')
        temp['phone_number'] = req.POST.get('phone_number')
        temp['job_title'] = req.POST.get('job_title')
        if req.user.is_authenticated:
            temp['user'] = req.user

        print(temp)
        form = SummitForm(temp)

        if form.is_valid():
            form.save()
            return redirect(reverse("core:summit"))
        else:
            print(form.errors)

    if  lang == None:
        
        return redirect(
            reverse("core:summit", args=["en"])
        )
    
    summits = models.Summit.objects.all()
    speaker = models.Speakers.objects.all()
    context = {
        "lang" : lang         ,
        "active" : "summits",
        "summits" : summits,
        "speakers" : speaker,
    }
    return render(req, "pages/summit.html", context)


def summit_detail(req:HttpRequest, lang=None, pk:int=None) -> HttpResponse:
    
    if pk == None:
        return redirect(
            reverse("core:summit", args=["en"])
        )
    if  lang == None:
        return redirect(
            reverse("core:summit_detail", args=["en", pk])
        )
    
    summit = models.Summit.objects.get(pk=pk)
    summits = summits.exclude(pk=pk)
    context = {
        "lang"     : lang       ,
        "active"   : "summits"  ,
        "summit"   : summit ,
        "others"   : summits  ,
    }
    return  render(req, "pages/summit_detail.html", context=context)


def summit_ticket(req:HttpRequest, lang=None, pk:int=None) -> HttpResponse:
    
    if pk == None:
        return redirect(
            reverse("core:summit_ticket", args=["en"])
        )
    if  lang == None:
        return redirect(
            reverse("core:summit_ticket", args=["en", pk])
        )
    
    summit = models.Summit.objects.get(pk=pk)
    summits = summits.exclude(pk=pk)
    context = {
        "lang"     : lang       ,
        "active"   : "summits"  ,
        "summit"   : summit ,
        "others"   : summits  ,
    }
    return  render(req, "pages/summit_ticket.html", context=context)



def speaker(req: HttpRequest, lang=None, pk: int=None) -> HttpResponse:

    if pk == None:
        return redirect(
            reverse("core:summit", args=["en"])
        )
    if lang == None:
        return redirect(
            reverse("core:speaker", args=["en", pk])
        )
    try:
        speaker = models.Speakers.objects.get(pk=pk)
    except:
        return redirect(
            reverse("core:summit", args=["en"]) 
        )
    context = {
        "lang"     : lang       ,
        "active"   : "summits"  ,
        "speaker"  : speaker ,

    }
    return  render(req, "pages/speaker.html", context=context)



def check_qr_valid_or_not(request, uuid=None):
    if request.user.is_staff or request.user.is_superuser:
        if uuid is None:
            return redirect(reverse("core:landing", args=["en"]))

        try:
            ticket = models.QrcodeForTicket.objects.get(uuid=uuid)
        except models.QrcodeForTicket.DoesNotExist:
            return render(request, 'global/qrcode_response.html', {'response': 'This ticket does not exist', 'status': 'error'})

        if ticket.summitticket.is_used:
            return render(request, 'global/qrcode_response.html', {'response': mark_safe(f'Ticket is already used  <h1> {ticket.summitticket.name} </h1>'), 'status': 'info'})  

        ticket.summitticket.is_used = True
        ticket.summitticket.save()
        return render(request, 'global/qrcode_response.html', {'response': mark_safe(f'Ticket is valid, welcome <h1> {ticket.summitticket.name} </h1>'), 'status': 'success'})   

    return render(request, 'global/qrcode_response.html', {'response': 'You are not allowed here', 'status': 'error'})

"qrcode_response.html"