# Generated by Django 5.0.10 on 2025-02-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_app', '0006_fb_oauth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fb_oauth',
            name='business_profiles',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
