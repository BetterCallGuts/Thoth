# Generated by Django 5.0.6 on 2024-07-17 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_summitticket_did_he_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='summitticket',
            name='sended_mail',
            field=models.BooleanField(default=False),
        ),
    ]
