# Generated by Django 5.0.10 on 2025-02-20 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('facebook_app', '0004_alter_fb_oauth_ad_accounts_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FB_Oauth',
        ),
    ]
