from django.db import models
from django.utils import timezone
from social_auth.models import BaseModel,SocialUser

class LinkedinAuth(BaseModel):
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    expires_in = models.CharField(max_length=520, null=True, blank=True)
    social_user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_auth', on_delete=models.CASCADE)
    class Meta:
        db_table = "Linkedin_auth"


class LinkedinCountries(BaseModel):
    load_datetime = models.DateTimeField(auto_now_add=True, null=True)
    locale_country = models.CharField(max_length=4, null=True)
    locale_language = models.CharField(max_length=4, null=True)
    country_name = models.CharField(max_length=64, null=True)
    country_group = models.CharField(max_length=32, null=True)
    urn = models.CharField(max_length=32, null=True)
    country_code = models.CharField(max_length=4, null=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_countries', on_delete=models.CASCADE)

    class Meta:
        db_table = "Linkedin_Countries"

class LinkedinCountryGroups(BaseModel):
    load_datetime = models.DateTimeField(null=True, blank=True, auto_now_add=True,)
    urn = models.CharField(max_length=32, null=True, blank=True)
    locale_country = models.CharField(max_length=4, null=True, blank=True)
    locale_language = models.CharField(max_length=4, null=True, blank=True)
    country_group = models.CharField(max_length=16, null=True, blank=True)
    country_group_code = models.CharField(max_length=4, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_country_groups', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Country_Groups'


class LinkedinFollowers(BaseModel):
    load_datetime = models.DateTimeField(null=True, blank=True)
    organic_follower_count = models.IntegerField(null=True, blank=True)
    paid_follower_count = models.IntegerField(null=True, blank=True)
    data_type = models.CharField(max_length=50, null=True, blank=True)
    data_type_id = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_followers', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Followers'


class LinkedinFollowersGainStatistics(BaseModel):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    organic_follower_gain = models.BigIntegerField(null=True, blank=True)
    paid_follower_gain = models.BigIntegerField(null=True, blank=True)
    organizational_entity = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_followersGain_statistics', on_delete=models.CASCADE)
    class Meta:
        db_table = 'Linkedin_FollowersGain_Statistics'



class LinkedinFunctions(BaseModel):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    function_id = models.BigIntegerField(null=True, blank=True)
    function_name = models.CharField(max_length=64, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_functions', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Functions'


class LinkedinIndustries(BaseModel):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    industry_id = models.BigIntegerField(null=True, blank=True)
    industry_name = models.CharField(max_length=64, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_industries', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Industries'


class LinkedinLocation(BaseModel):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=25, null=True, blank=True)
    geo_id = models.BigIntegerField(null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_location', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Location'

class LinkedinPostsStatistics(BaseModel):
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
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_posts_statistics', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Posts_Statistics'



class LinkedinRegions(BaseModel):
    locale_country = models.CharField(max_length=4, null=True, blank=True)
    locale_language = models.CharField(max_length=4, null=True, blank=True)
    value = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    region_id = models.BigIntegerField(null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    states = models.TextField(null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_regions', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Linkedin_Regions'


class LinkedinSeniorities(BaseModel):
    load_datetime = models.DateTimeField(default=timezone.now, null=True, blank=True)
    urn = models.CharField(max_length=32, null=True, blank=True)
    seniority_id = models.BigIntegerField(null=True, blank=True)
    seniority_name = models.CharField(max_length=16, null=True, blank=True)
    user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_linkedin_seniorities', on_delete=models.CASCADE)
    class Meta:
        db_table = 'Linkedin_Seniorities'