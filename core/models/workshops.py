from django.db import models
from datetime import datetime










class WorkShopsCategory(models.Model):
    name_en = models.CharField(max_length=100)
    name_ar= models.CharField(max_length=100)
    description_en = models.TextField()
    description_ar = models.TextField()
    banner         = models.ImageField(upload_to="workshopscategory_banner", null=True, blank=True)
    def  more(self):
        return "more"

    def __str__(self):
        return self.name_en




class WorkShops(models.Model):

    category = models.ForeignKey(WorkShopsCategory, on_delete=models.CASCADE)

    name_en = models.CharField(max_length=100)
    name_ar= models.CharField(max_length=100)

    description = models.TextField()

    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name_en
    
    class Meta:
        verbose_name = "Workshops"
        verbose_name_plural = "Workshops"
