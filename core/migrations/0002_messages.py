# Generated by Django 5.0.6 on 2024-07-08 08:22

import datetime
import django_ckeditor_5.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', django_ckeditor_5.fields.CKEditor5Field(blank=True)),
                ('created_in', models.DateField(default=datetime.datetime.now, editable=False)),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
