# Generated by Django 5.0.10 on 2025-02-20 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0005_instagrammediainsight_social_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagrammediainsight',
            name='social_user',
        ),
        migrations.RemoveField(
            model_name='instagrampagestatisticslifetime',
            name='social_user',
        ),
    ]
