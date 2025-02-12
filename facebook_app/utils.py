from .models import FB_Oauth

def get_fb_oauth_details(email):
    """
    Retrieve the latest Facebook OAuth details based on the provided email.
    Returns a dictionary of details or None if no data is found.
    """
    print(email,'email>>>>>>>>>')
    fb_oauth = FB_Oauth.objects.filter(social_user__email=email).order_by('-id').first()
    print(fb_oauth,'hereeeeeeeeeee')
      # Get the latest entry
    if not fb_oauth:
        return None
    return {
        "access_token": fb_oauth.access_token,
        "page_id": fb_oauth.page_id,
        "ad_account": fb_oauth.ad_accounts,
        "business_profiles": fb_oauth.business_profiles,
        "instagram_account": fb_oauth.instagram_account,
    }

def get_social_user(email):
    """
    Retrieves the SocialUser associated with the given access token.
    Args:
        access_token (str): LinkedIn API access token.
    Returns:
        SocialUser: The associated social user.
    """
    auth_instance = FB_Oauth.objects.filter(social_user__email=email).first()
    if auth_instance:
        return auth_instance.social_user
    return None
