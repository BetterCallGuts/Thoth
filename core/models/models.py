from django.db import models
from datetime import datetime
from django.core.validators import FileExtensionValidator
from django.utils.html  import mark_safe
from django.contrib.auth.models   import User

import qrcode
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files import File
import uuid

from django.urls import reverse
from django.conf import settings

from django_ckeditor_5.fields import CKEditor5Field

class Instructor(models.Model):

    name_ar = models.CharField(max_length=255, verbose_name="اسم المدرس")
    name_en = models.CharField(max_length=255, verbose_name="name in english")
    photo_banner = models.ImageField(upload_to="instructors_photos", blank=True, null=True)
    time_added   = models.DateField(default=datetime.now, editable=False)
    speciality   = models.ForeignKey("CourseCategory", on_delete=models.SET_NULL, null=True, blank=True)
    bio_en        = models.TextField(null=True, blank=True)
    bio_ar        = models.TextField(null=True, blank=True) 

    def show_image(self):
        
        return mark_safe(f"<img style='width:300px;' src='{self.photo_banner.url}'  alt='{self.name_en}' />")
    def more(self):
        return "more"
    show_image.short_description = "photo for him"
    def __str__(self):

        return f"{self.name_ar}"
    class Meta:
        verbose_name        = "المدرس"
        verbose_name_plural = "المدرسين"
        

class CourseCategory(models.Model):
    name_en = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    banner  = models.ImageField(upload_to="course_categories", blank=True, null=True)


    def more(self):
        return "more"
    def __str__(self):
        return f"{self.name_ar} || {self.name_en}"
    class Meta:
        verbose_name =        "نوع  كورس"
        verbose_name_plural = "انواع الكورسات"
        

class Courses(models.Model):

    
    category   = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    banner     = models.ImageField(verbose_name="thumbnail", upload_to="courses_banner_general", blank=True, null=True)
    instructor = models.ForeignKey(Instructor, verbose_name="المدرس", on_delete=models.CASCADE)
    name_ar    = models.CharField(max_length=255, verbose_name="اسم كورس")
    name_en    = models.CharField(max_length=255, verbose_name="اسم الكورس انجليزي")
    description_en= models.TextField(null=True, blank=True)
    description_ar= models.TextField(null=True, blank=True, verbose_name="وصف بالعربي")
    price         = models.FloatField(default=0)
    isonsale      = models.BooleanField(default=False)
    onsale        = models.FloatField(default=0)
    trailer       = models.FileField(upload_to="course_trailer", verbose_name="الفيديو",
    validators=[FileExtensionValidator(
        allowed_extensions=["mp4", "webm", "avi", "AVI", "WebM"])],
    help_text='Allowed : "mp4", "webm", "avi", "AVI", "WebM" ', null=True, blank=True)  

    def __str__(self):
        return f"{self.instructor}|{self.name_ar}"
    class Meta:
        
        verbose_name = "كورس"
        verbose_name_plural = "كورسات"
    def more(self):
        return "انقر للمزيد"
    def show_image(self):
        
        return mark_safe(f"<img style='width:300px;' src='{self.banner.url}'  alt='{self.name_en}' />")
    more.short_description = "انقر للمزيد"
    show_image.short_description = "Thumbnail"

class Ep(models.Model):
    course    = models.ForeignKey(Courses, on_delete=models.CASCADE)
    banner    = models.ImageField(verbose_name="thumbnail", upload_to="courses_banner", blank=True, null=True)
    video     = models.FileField(upload_to="course", verbose_name="الفيديو",
    validators=[FileExtensionValidator(
        allowed_extensions=["mp4", "webm", "avi", "AVI", "WebM"])],
    help_text='Allowed : "mp4", "webm", "avi", "AVI", "WebM" ')
    name_ar   = models.CharField(max_length=255, verbose_name="اسم الحلقة عربي")
    name_en   = models.CharField(max_length=255, verbose_name="اسم الحلقة انجليزي")
    descr_en  = models.TextField(blank=True, null=True, verbose_name="description ")
    descr_ar  = models.TextField(blank=True, null=True, verbose_name="وصف ")
    created_in= models.DateField(default=datetime.now, editable=False)



class Meetup(models.Model):
    
    banner = models.ImageField(upload_to="meetups_banner", blank=True, null=True)
    insctructors = models.ManyToManyField(Instructor    )
    meetupname_en= models.CharField(max_length=255      )
    meetupname_ar= models.CharField(max_length=255      )
    time_added   = models.DateField(default=datetime.now)
    time_event_starts_in = models.DateField(default=datetime.now)
    is_finished  = models.BooleanField(default=False    )
    price         = models.FloatField(default=0)
    isonsale      = models.BooleanField(default=False)
    onsale        = models.FloatField(default=0)
    is_sold      = models.BooleanField(default=False    )
    description_en= models.TextField(null=True, blank=True)
    description_ar= models.TextField(null=True, blank=True, verbose_name="وصف بالعربي")
    def __str__(self):
        return f"{self.meetupname_en} || {self.meetupname_ar}"
    class Meta:
        verbose_name_plural = "Meetups"
        verbose_name        = "Meetup"
    
    def more(self):
        return "more"



class MeetupTicket(models.Model):
     
    user    = models.ForeignKey(User,   on_delete=models.CASCADE, null=True , blank=True)
    meetup  = models.ForeignKey(Meetup, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    howmany = models.IntegerField(default=0)    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

    class Meta:
        verbose_name_plural =  "MeetupTickets"
        verbose_name        =  "meetup Ticket"
    


class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    class Meta:
        verbose_name_plural =  "UserCourses"
        verbose_name        =  "UserCourses"




class Speakers(models.Model):
    name_ar = models.CharField(max_length=255, verbose_name="اسم المتحدث")
    name_en = models.CharField(max_length=255, verbose_name="name in english")
    photo_banner = models.ImageField(upload_to="speakers_photos", blank=True, null=True)
    personal_photo = models.ImageField(upload_to="speakers_photos", blank=True, null=True)  
    bio_en        = models.TextField(null=True, blank=True)

    bio_ar        = models.TextField(null=True, blank=True)
    short_bio_en = models.TextField(null=True, blank=True)
    short_bio_ar = models.TextField(null=True, blank=True)
    instgram_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    facebook_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name_en}"
    
    def more(self):
        return "more"
class Summit(models.Model):

    Speakers = models.ManyToManyField(Speakers, blank=True)
    banner = models.ImageField(upload_to="summits_banner", blank=True, null=True)
    name_ar = models.CharField(max_length=255, verbose_name="اسم المؤتمر")
    name_en = models.CharField(max_length=255, verbose_name="name in english")
    description_en = models.TextField(null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    isonsale = models.BooleanField(default=False)
    onsale = models.FloatField(default=0)
    time_added   = models.DateField(default=datetime.now)
    time_event_starts_in = models.DateField(default=datetime.now)
    is_finished  = models.BooleanField(default=False    )
    trailer = models.FileField(upload_to="summit_trailer", verbose_name="الفيديو",
                               validators=[FileExtensionValidator(
                                   allowed_extensions=["mp4", "webm", "avi", "AVI", "WebM"])],
                               help_text='Allowed : "mp4", "webm", "avi", "AVI", "WebM" ', null=True, blank=True)
    
    def more(self):
        return "more"
    def __str__(self):
        return f"{self.name_en}"
    class Meta:
        verbose_name        = "Summit"
        verbose_name_plural = "Summits"

class SummitTicket(models.Model):
     
    user    = models.ForeignKey(User,   on_delete=models.SET_NULL, null=True , blank=True)

    summit  = models.ForeignKey(Summit, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    job_title = models.CharField(max_length=255, null=True, blank=True)

    # howmany = models.IntegerField(default=0)    
    
    def more(self):
        return "more"
    def __str__(self):
        return f"{self.name or self.pk}"
    

class Messages(models.Model):

    Text = CKEditor5Field(blank=True)
    created_in = models.DateField(default=datetime.now, editable=False)
    
    def __str__(self):
        return f"{self.Text}"
    class Meta:
        verbose_name        = "Message"
        verbose_name_plural = "Messages"


class QrcodeForTicket(models.Model):

    summitticket = models.ForeignKey(SummitTicket, on_delete=models.CASCADE)
    qrcode = models.ImageField(upload_to="qrcode", blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    def __str__(self):
        return f"{self.summitticket.name}"
    def save(self, *args, **kwargs):
        # Generate QR code
        qrcode_img = qrcode.make(f"{settings.SITE_DOMAIN}{reverse('core:check_qr_valid_or_not', args=[self.uuid])}")  # you can use any data, e.g., self.description
        canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.summitticket.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    def chose_message(self):
                        mesgs = Messages.objects.all()
                        return mark_safe(f""" 
                        <select  
                                        style="width:300px;"
                                        
                                        class="select2-selection__rendered" name="message" id="messageSp">
                                        {[f"<option value={mesg.id}>{mesg}</option>" for mesg in mesgs]}

                        <select>



""")
    def send_mail(self):

        return mark_safe(f"""

<form id="myForm" action="{reverse('core:send_test_email')}" method="get">
 

<button id="mysssbutton" >Send</button>
</form>
 """ +"""
<script> 
 document.addEventListener('DOMContentLoaded', function () {
delete this_is_my_spicial_form_omarhosnayAbdelmotelb;
 var this_is_my_spicial_form_omarhosnayAbdelmotelb = document.getElementById('myForm');
        const id_email = document.getElementById('id_email');
        const messageSp = document.getElementById('messageSp'); // Ensure this exists in your HTML
        let buttondasds = document.getElementById('mysssbutton');
       
        buttondasds.addEventListener('click', function (event) {
            // Prevent the default form submission
            event.preventDefault();

            // Check if the id_email has a value
            if (id_email && id_email.value) {
                // Create a hidden input element
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'hiddenEmail'; // Set the name for the hidden input
                hiddenInput.value = id_email.value;
""" + f"""
const pk = document.createElement('input');
                pk.type = 'hidden';
                pk.name = 'pk'; // Set the name for the hidden input
                pk.value = {self.pk}; // Set the value for the hidden input
""" + "" + """
""" + """

                // Append the hidden input to the form
                this_is_my_spicial_form_omarhosnayAbdelmotelb.appendChild(hiddenInput);
                this_is_my_spicial_form_omarhosnayAbdelmotelb.appendChild(pk);

                // Optionally, create another hidden input for 'messageSp' value if needed
                if (messageSp && messageSp.value) {
                    const hiddenMessageInput = document.createElement('input');
                    hiddenMessageInput.type = 'hidden';
                    hiddenMessageInput.name = 'hiddenMessage';
                    hiddenMessageInput.value = messageSp.value;
                    this_is_my_spicial_form_omarhosnayAbdelmotelb.appendChild(hiddenMessageInput);
                }
            }

            // Now, submit the form
            console.log(this_is_my_spicial_form_omarhosnayAbdelmotelb.action)
            console.log(this_is_my_spicial_form_omarhosnayAbdelmotelb.values)
            console.log("we are here")
             this_is_my_spicial_form_omarhosnayAbdelmotelb.submit();
        });
            });
</script>
                         
                         """)
    def show_image(self):
        return mark_safe(f"<img style='width:300px;' src='{self.qrcode.url}'  alt='{self.summitticket.name}' />")
    def __str__(self):
        return f"{self.summitticket.name}"
    class Meta:
        verbose_name        = "SummitTicket"
        verbose_name_plural = "SummitTickets"



    send_mail.short_description = "Click on button to send"