from django.db import models
import requests
from social_auth.models import BaseModel,SocialUser

class InstagramMediaInsight(BaseModel):
    ig_id = models.CharField(max_length=50, unique=True, verbose_name="Instagram Post ID")
    post_date = models.CharField(max_length=100, null=True, blank=True, verbose_name="Post Date")  # Stored as text
    email = models.CharField(max_length=255, null=True, blank=True,)
    media_type = models.CharField(max_length=50, verbose_name="Media Type", null=True, blank=True)
    comments_count = models.CharField(max_length=20, default="0", verbose_name="Comments Count", null=True, blank=True)  # Converted to text
    like_count = models.CharField(max_length=20, default="0", verbose_name="Like Count", null=True, blank=True)  # Converted to text
    permalink = models.CharField(max_length=500, verbose_name="Permalink", null=True, blank=True)
    username = models.CharField(max_length=100, verbose_name="Username", null=True, blank=True)
    caption = models.TextField(null=True, blank=True, verbose_name="Caption")
    media_product_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Media Product Type")
    is_comment_enabled = models.CharField(max_length=10, default="True", verbose_name="Comments Enabled", null=True, blank=True)  # Stored as "True"/"False"
    media_url = models.CharField(max_length=500, null=True, blank=True, verbose_name="Media URL")

    # Insights (Stored as text)
    impressions = models.CharField(max_length=20, default="0", verbose_name="Impressions", null=True, blank=True)
    reach = models.CharField(max_length=20, default="0", verbose_name="Reach", null=True, blank=True)
    profile_visits = models.CharField(max_length=20, default="0", verbose_name="Profile Visits")
    profile_activity = models.CharField(max_length=20, default="0", verbose_name="Profile Activity", null=True, blank=True)
    replies = models.CharField(max_length=20, default="0", verbose_name="Replies", null=True, blank=True)
    saved = models.CharField(max_length=20, default="0", verbose_name="Saved", null=True, blank=True)
    video_views = models.CharField(max_length=20, default="0", verbose_name="Video Views", null=True, blank=True)
    shares = models.CharField(max_length=20, default="0", verbose_name="Shares", null=True, blank=True)
    total_interactions = models.CharField(max_length=20, default="0", verbose_name="Total Interactions", null=True, blank=True)
    follows = models.CharField(max_length=20, default="0", verbose_name="Follows", null=True, blank=True)

    created_at = models.CharField(max_length=100, verbose_name="Created At", null=True, blank=True)  # Stored as text
    updated_at = models.CharField(max_length=100, verbose_name="Updated At", null=True, blank=True)  # Stored as text

    data_created_date = models.CharField(max_length=255, null=True, blank=True)
    data_created_time = models.CharField(max_length=255, null=True, blank=True)

    social_user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_Instagram_Media_Insights', on_delete=models.CASCADE)


    class Meta:
        db_table = 'Instagram_Media_Insights'


class InstagramPageInsight(BaseModel):
    end_time = models.DateTimeField(null=True, blank=True)  # End time of the insights
    follower_count = models.IntegerField(default=0, null=True, blank=True)  # Follower count
    impressions = models.IntegerField(default=0, null=True, blank=True)  # Impressions
    reach = models.IntegerField(default=0, null=True, blank=True)  # Reach
    page_id = models.CharField(max_length=255, null=True, blank=True)  # Facebook Page ID
    email = models.EmailField(max_length=254, null=True, blank=True)  # Email of the user
    data_created_date = models.DateField(auto_now_add=True)  # Date when data was created
    data_created_time = models.TimeField(auto_now_add=True)  # Time when data was created
    social_user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_Instagram_Page_Insight', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Instagram_Page_Insight'


class InstagramPageStatisticsLifetime(BaseModel):
    id = models.CharField(max_length=50, primary_key=True)  # Instagram Page ID
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    followers_count = models.CharField(max_length=50, null=True, blank=True)  # Changed to CharField
    follows_count = models.CharField(max_length=50, null=True, blank=True)  # Changed to CharField
    media_count = models.CharField(max_length=50, null=True, blank=True)  # Changed to CharField
    website = models.CharField(max_length=255, null=True, blank=True)  # Changed to CharField
    profile_picture_url = models.CharField(max_length=500, null=True, blank=True)
    biography = models.CharField(max_length=2000, null=True, blank=True)  # Changed to CharField
    created_at = models.CharField(max_length=50, null=True, blank=True)  # Store timestamp as a string
    email = models.EmailField(max_length=254, null=True, blank=True)  # Email of the user
    data_created_date = models.DateField(auto_now_add=True)  # Date when data was created
    data_created_time = models.TimeField(auto_now_add=True)  # Time when data was created
    social_user = models.ForeignKey(SocialUser, null=True, blank=True, related_name='user_Instagram_Page_Statistics_Lifetime', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Instagram_Page_Statistics_Lifetime'



