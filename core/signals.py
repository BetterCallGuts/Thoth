from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import models
import os


@receiver(post_save, sender=models.SummitTicket)
def create_qrcode(sender, instance, created, **kwargs):
    if created:

        qr = models.QrcodeForTicket(summitticket=instance)
        qr.save()


@receiver(post_delete, sender=models.QrcodeForTicket)
def delete_image_on_model_delete(sender, instance, **kwargs):
    if instance.qrcode:
        if os.path.isfile(instance.qrcode.path):
            try:
                os.remove(instance.qrcode.path)
            except Exception as e:
                print(e)