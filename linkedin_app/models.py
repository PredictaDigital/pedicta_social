from django.db import models
from django.utils import timezone

class LinkedinCountries(models.Model):
    load_datetime = models.DateTimeField(auto_now_add=True, null=True)
    locale_country = models.CharField(max_length=4, null=True)
    locale_language = models.CharField(max_length=4, null=True)
    country_name = models.CharField(max_length=64, null=True)
    country_group = models.CharField(max_length=32, null=True)
    urn = models.CharField(max_length=32, null=True)
    country_code = models.CharField(max_length=4, null=True)

    class Meta:
        db_table = "Linkedin_Countries"

class LinkedinCountryGroups(models.Model):
    load_datetime = models.DateTimeField(null=True, blank=True, auto_now_add=True,)
    urn = models.CharField(max_length=32, null=True, blank=True)
    locale_country = models.CharField(max_length=4, null=True, blank=True)
    locale_language = models.CharField(max_length=4, null=True, blank=True)
    country_group = models.CharField(max_length=16, null=True, blank=True)
    country_group_code = models.CharField(max_length=4, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Country_Groups'


class LinkedinFollowers(models.Model):
    load_datetime = models.DateTimeField(null=True, blank=True)
    organic_follower_count = models.IntegerField(null=True, blank=True)
    paid_follower_count = models.IntegerField(null=True, blank=True)
    data_type = models.CharField(max_length=50, null=True, blank=True)
    data_type_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Followers'


class LinkedinFollowersGainStatistics(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    organic_follower_gain = models.BigIntegerField(null=True, blank=True)
    paid_follower_gain = models.BigIntegerField(null=True, blank=True)
    organizational_entity = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_FollowersGain_Statistics'



class LinkedinFunctions(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    function_id = models.BigIntegerField(null=True, blank=True)
    function_name = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Functions'


class LinkedinIndustries(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    industry_id = models.BigIntegerField(null=True, blank=True)
    industry_name = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Industries'


class LinkedinLocation(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=25, null=True, blank=True)
    geo_id = models.BigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Location'

class LinkedinPostsStatistics(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    post_id = models.CharField(max_length=100, null=True, blank=True)
    organizational_entity = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    commentary = models.TextField(null=True, blank=True)
    is_reshare_disabled_by_author = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    lifecycle_state = models.CharField(max_length=50, null=True, blank=True)
    last_modified_at = models.DateTimeField(null=True, blank=True)
    visibility = models.CharField(max_length=50, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    feed_distribution = models.CharField(max_length=50, null=True, blank=True)
    is_edited_by_author = models.CharField(max_length=10, null=True, blank=True)
    unique_impressions_count = models.IntegerField(null=True, blank=True)
    share_count = models.IntegerField(null=True, blank=True)
    engagement = models.IntegerField(null=True, blank=True)
    click_count = models.IntegerField(null=True, blank=True)
    like_count = models.IntegerField(null=True, blank=True)
    comment_count = models.IntegerField(null=True, blank=True)
    impression_count = models.IntegerField(null=True, blank=True)
    engagement_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    click_through_rate = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Posts_Statistics'



class LinkedinRegions(models.Model):
    locale_country = models.CharField(max_length=4, null=True, blank=True)
    locale_language = models.CharField(max_length=4, null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    region_id = models.BigIntegerField(null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    states = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Regions'


class LinkedinSeniorities(models.Model):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    seniority_id = models.BigIntegerField(null=True, blank=True)
    seniority_name = models.CharField(max_length=16, null=True, blank=True)

    class Meta:
        db_table = 'Linkedin_Seniorities'