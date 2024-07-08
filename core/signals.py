from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import models



@receiver(post_save, sender=models.SummitTicket)
def create_qrcode(sender, instance, created, **kwargs):
    if created:

        qr = models.QrcodeForTicket(summitticket=instance)
        qr.save()
