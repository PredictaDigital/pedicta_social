# helpers.py
import requests
from .models import *
from django.utils import timezone
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
LINKEDIN_API_URL = os.getenv("LINKEDIN_API_URL")
LINKEDIN_APP_VERSION = os.getenv("LINKEDIN_APP_VERSION")

def get_social_user_from_token(access_token):
    """
    Retrieves the SocialUser associated with the given access token.
    Args:
        access_token (str): LinkedIn API access token.
    Returns:
        SocialUser: The associated social user.
    """
    auth_instance = LinkedinAuth.objects.filter(access_token=access_token).first()
    if auth_instance:
        return auth_instance.social_user
    return None




def fetch_and_insert_linkedin_country_data(access_token):
    """
    Fetches LinkedIn country data and inserts it into the database.
    Args:
        access_token (str): LinkedIn API access token.
        app_version (str): LinkedIn API version.
    """
    analytics_url = f'{LINKEDIN_API_URL}/v2/countries'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from LinkedIn API")

    analytics_data = response.json()
    user = get_social_user_from_token(access_token)
    countries = []
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            country_data = {
                'locale_country': element['name']['locale']['country'],
                'locale_language': element['name']['locale']['language'],
                'country_name': element['name']['value'],
                'country_group': element.get('countryGroup'),
                'urn': element.get('$URN'),
                'country_code': element.get('countryCode'),
                'user': user
            }
            countries.append(country_data)

    # Insert data into the database
    for country in countries:
        LinkedinCountries.objects.create(**country)



def fetch_and_insert_linkedin_country_group_data(access_token):
    """
    Fetches LinkedIn country group data and inserts it into the database.

    Args:
        access_token (str): LinkedIn API access token.
        app_version (str): LinkedIn API version.
    """
    analytics_url = f'{LINKEDIN_API_URL}/v2/countryGroups'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from LinkedIn API")

    analytics_data = response.json()
    user = get_social_user_from_token(access_token)

    country_groups = []
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            country_group_data = {
                'urn': element.get('$URN'),
                'locale_country': element['name']['locale']['country'],
                'locale_language': element['name']['locale']['language'],
                'country_group': element['name']['value'],
                'country_group_code': element.get('countryGroupCode'),
                'user':user
            }
            country_groups.append(country_group_data)

    # Insert data into the database
    for country_group in country_groups:
        LinkedinCountryGroups.objects.create(**country_group)


def fetch_and_insert_linkedin_followers_data(access_token):
    """
    Fetches LinkedIn followers data and inserts it into the database.

    Args:
        access_token (str): LinkedIn API access token.
        app_version (str): LinkedIn API version.
    """
    analytics_url = f'{LINKEDIN_API_URL}/v2/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:13701784'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from LinkedIn API")

    # Truncate the table
    LinkedinFollowers.objects.all().delete()

    analytics_data = response.json()
    user = get_social_user_from_token(access_token)

    # Get the current datetime
    load_datetime = timezone.now()

    # Iterate over the data and insert into the database
    for element in analytics_data.get('elements', []):
        if 'followerCountsByStaffCountRange' in element:
            for item in element['followerCountsByStaffCountRange']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'staffCountRange',
                    'data_type_id': item['staffCountRange'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsByFunction' in element:
            for item in element['followerCountsByFunction']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'Function',
                    'data_type_id': item['function'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsBySeniority' in element:
            for item in element['followerCountsBySeniority']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'Seniority',
                    'data_type_id': item['seniority'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsByAssociationType' in element:
            for item in element['followerCountsByAssociationType']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'AssociationType',
                    'data_type_id': item['associationType'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsByIndustry' in element:
            for item in element['followerCountsByIndustry']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'Industry',
                    'data_type_id': item['industry'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsByGeo' in element:
            for item in element['followerCountsByGeo']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'Location',
                    'data_type_id': item['geo'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)

        if 'followerCountsByGeoCountry' in element:
            for item in element['followerCountsByGeoCountry']:
                data = {
                    'load_datetime': load_datetime,
                    'organic_follower_count': item['followerCounts']['organicFollowerCount'],
                    'paid_follower_count': item['followerCounts']['paidFollowerCount'],
                    'data_type': 'Country',
                    'data_type_id': item['geo'],
                    'user':user
                }
                LinkedinFollowers.objects.create(**data)



def fetch_and_insert_linkedin_followers_gain_data(access_token):

    # Define the API endpoint
    analytics_url = (
        f'{LINKEDIN_API_URL}/rest/organizationalEntityFollowerStatistics'
        f'?q=organizationalEntity'
        f'&organizationalEntity=urn:li:organization:13701784'
        f'&timeIntervals.timeGranularityType=DAY'
        f'&timeIntervals.timeRange.start=1710028800000'
        f'&timeIntervals.timeRange.end=1716854400000'
    )
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION,
    }

    # Retrieve data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from LinkedIn API: {response.status_code} - {response.text}')
    analytics_data = response.json()

    user = get_social_user_from_token(access_token)

    # Iterate over the data and insert into the database
    for element in analytics_data.get('elements', []):
        if 'followerGains' in element:
            time_range_start = datetime.fromtimestamp(element['timeRange']['start'] / 1000)
            time_range_end = datetime.fromtimestamp(element['timeRange']['end'] / 1000)
            organic_follower_gain = element['followerGains'].get('organicFollowerGain')
            paid_follower_gain = element['followerGains'].get('paidFollowerGain')
            organizational_entity = element.get('organizationalEntity')

            # Prepare data for creation
            data = {
                'start_date': time_range_start.date(),
                'end_date': time_range_end.date(),
                'organic_follower_gain': organic_follower_gain,
                'paid_follower_gain': paid_follower_gain,
                'organizational_entity': organizational_entity,
                'user':user
            }

            # Create and save the new record
            LinkedinFollowersGainStatistics.objects.create(**data)



def fetch_and_insert_linkedin_functions_data(access_token):
    # Define the API endpoint
    analytics_url = f'{LINKEDIN_API_URL}/v2/functions'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }
    
    # Retrieve data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from LinkedIn API: {response.status_code} - {response.text}')
    
    analytics_data = response.json()

    user = get_social_user_from_token(access_token)
    
    # Prepare data for insertion
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            urn = element.get('$URN')
            function_id = element.get('id')
            function_name = element['name']['localized'].get('en_US')

            # Prepare data dictionary for model creation
            data = {
                'load_datetime': timezone.now(),
                'urn': urn,
                'function_id': function_id,
                'function_name': function_name,
                'user':user
            }
            # Insert data into the model
            LinkedinFunctions.objects.create(**data)



def fetch_and_insert_linkedin_industries_data(access_token):
    # Define the API endpoint
    analytics_url = f'{LINKEDIN_API_URL}/v2/industries'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }
    
    # Retrieve data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from LinkedIn API: {response.status_code} - {response.text}')
    
    analytics_data = response.json()

    user = get_social_user_from_token(access_token)
    
    # Prepare data for insertion
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            urn = element.get('$URN')
            industry_id = element.get('id')
            industry_name = element['name']['localized'].get('en_US')

            # Prepare data dictionary for model creation
            data = {
                'load_datetime': timezone.now(),
                'urn': urn,
                'industry_id': industry_id,
                'industry_name': industry_name,
                'user':user
            }
            # Insert data into the model
            LinkedinIndustries.objects.create(**data)


def fetch_and_insert_linkedin_regions_data(access_token):
    # Define the API endpoint for retrieving regions data
    analytics_url = f'{LINKEDIN_API_URL}/v2/regions'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    # Retrieve regions data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        # Handle the error if the request fails
        print(f"Failed to retrieve data: {response.status_code}")
        return

    analytics_data = response.json()

    user = get_social_user_from_token(access_token)

    # Iterate over the data and insert records into the database
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            name_data = element['name']
            states_data = element.get('States', {})
            state_info = states_data.get('states', {}).get('state', '')

            # Prepare data for insertion into the model
            data = {
                'locale_country': name_data.get('locale', {}).get('country', ''),
                'locale_language': name_data.get('locale', {}).get('language', ''),
                'value': element.get('value', ''),
                'country': element.get('country', ''),
                'region_id': element.get('id', None),
                'urn': element.get('$URN', ''),
                'states': state_info,
                'user':user
            }

            # Insert data into the LinkedInRegionsKS model
            LinkedinRegions.objects.create(**data)



def fetch_and_insert_linkedin_seniorities_data(access_token):
    # Define the API endpoint for retrieving seniorities data
    analytics_url = f'{LINKEDIN_API_URL}/v2/seniorities'

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    # Retrieve seniority data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve data: {response.status_code}")
        return

    analytics_data = response.json()

    user = get_social_user_from_token(access_token)

    # Truncate the table
    LinkedinSeniorities.objects.all().delete()

    # Iterate over the data and insert records into the database
    for element in analytics_data.get('elements', []):
        if 'name' in element:
            data = {
                'urn': element.get('$URN', ''),
                'seniority_id': element.get('id', None),
                'seniority_name': element.get('name', {}).get('localized', {}).get('en_US', ''),
                'load_datetime': timezone.now(),
                'user':user
            }

            # Use Django ORM to create the record using the data dictionary
            LinkedinSeniorities.objects.create(**data)


def fetch_and_insert_linkedin_location_data(access_token):
    # Define the API endpoint for retrieving follower count by geo
    analytics_url = f'{LINKEDIN_API_URL}/rest/organizationalEntityFollowerStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:13701784'
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }
    
    # Retrieve the follower counts by geo data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from LinkedIn API: {response.status_code} - {response.text}')

    # Truncate the table
    LinkedinLocation.objects.all().delete()
    
    analytics_data = response.json()

    user = get_social_user_from_token(access_token)
    
    # Extract geo IDs from the follower counts
    geo_locations = []
    for element in analytics_data.get('elements', []):
        if 'followerCountsByGeo' in element:
            for item in element['followerCountsByGeo']:
                geo_id = item['geo']
                geo_locations.append(geo_id)

    geo_ids = [geo_id.split(':')[-1] for geo_id in geo_locations]
    geo_ids_str = ','.join(geo_ids)
    
    # Retrieve the geo data for the extracted geo IDs
    geo_url = f'{LINKEDIN_API_URL}/v2/geo?ids=List({geo_ids_str})'
    headers1 = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': '202304',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    geo_response = requests.get(geo_url, headers=headers1)
    geo_data = geo_response.json()
    
    # Prepare data for insertion into the model
    for result_id, result_info in geo_data.get('results', {}).items():
        geo_id = result_info.get('id')
        city = result_info.get('defaultLocalizedName', {}).get('value')
        
        # Prepare data dictionary for model creation
        data = {
            'load_datetime': timezone.now(),
            'urn': f'urn:li:geo:{geo_id}',
            'geo_id': geo_id,
            'city': city,
            'user':user
        }
        
        # Insert data into the model
        LinkedinLocation.objects.create(**data)



def fetch_and_insert_linkedin_posts_statistics(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION
    }

    organization_urn = 'urn:li:organization:13701784'

    # Define the URL for fetching posts
    posts_url = f'{LINKEDIN_API_URL}/rest/posts?author={organization_urn}&q=author&count=100&sortBy=LAST_MODIFIED'

    # Fetch posts
    response = requests.get(posts_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve posts: {response.status_code}")
        return

    posts_data = response.json()

    user = get_social_user_from_token(access_token)

    # Extract post IDs
    post_ids = [post['id'] for post in posts_data.get('elements', [])]

    # Fetch insights for each post ID
    insights = {}
    for post_id in post_ids:
        insights_url = f'{LINKEDIN_API_URL}/rest/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity={organization_urn}&shares={post_id}'
        response = requests.get(insights_url, headers=headers)
        if response.status_code == 200:
            insights_data = response.json()
            insights[post_id] = insights_data

    # Clear existing records
    LinkedinPostsStatistics.objects.all().delete()

    # Function to convert timestamp to datetime
    def convert_to_datetime(timestamp):
        return datetime.fromtimestamp(timestamp / 1000.0) if timestamp else None

    # Iterate over posts and insert into the database
    for post in posts_data.get('elements', []):
        post_id = post['id']
        insight_data = insights.get(post_id, {})
        insight_elements = insight_data.get('elements', [])

        # Ensure insight_elements is not empty before accessing index 0
        insight = insight_elements[0] if insight_elements else {}

        total_share_stats = insight.get('totalShareStatistics', {})
        organizational_entity = insight.get('organizationalEntity', '')

        # Calculate engagement and click-through rates
        click_count = total_share_stats.get('clickCount', 0)
        impression_count = total_share_stats.get('impressionCount', 0)
        engagement_rate = (total_share_stats.get('engagement', 0) * 100) if impression_count else 0
        click_through_rate = (click_count / impression_count * 100) if impression_count else 0

        # Prepare data dictionary
        data = {
            'post_id': post_id,
            'organizational_entity': organizational_entity,
            'author': post.get('author'),
            'commentary': post.get('commentary', ''),
            'is_reshare_disabled_by_author': post.get('isReshareDisabledByAuthor'),
            'created_at': convert_to_datetime(post.get('createdAt')),
            'lifecycle_state': post.get('lifecycleState'),
            'last_modified_at': convert_to_datetime(post.get('lastModifiedAt')),
            'visibility': post.get('visibility'),
            'published_at': convert_to_datetime(post.get('publishedAt')),
            'feed_distribution': post.get('distribution', {}).get('feedDistribution'),
            'is_edited_by_author': post.get('lifecycleStateInfo', {}).get('isEditedByAuthor', ''),
            'unique_impressions_count': total_share_stats.get('uniqueImpressionsCount', 0),
            'share_count': total_share_stats.get('shareCount', 0),
            'engagement': click_count + total_share_stats.get('commentCount', 0) + total_share_stats.get('likeCount', 0) + total_share_stats.get('shareCount', 0),
            'click_count': click_count,
            'like_count': total_share_stats.get('likeCount', 0),
            'comment_count': total_share_stats.get('commentCount', 0),
            'impression_count': impression_count,
            'engagement_rate': engagement_rate,
            'click_through_rate': click_through_rate,
            'load_datetime': timezone.now(),
            'user':user
        }
        # Create a new record using the data dictionary
        LinkedinPostsStatistics.objects.create(**data)


def fetch_and_insert_linkedin_followers_gain_data_separate(access_token):
    user = get_social_user_from_token(access_token)

    # Fetch the latest entry for the user
    latest_entry = LinkedinFollowersGainStatistics.objects.filter(user=user).order_by('-end_date').first()

    # Calculate start and end timestamps in epoch format
    if latest_entry:
        # If data exists, start from the latest end_date and go forward 60 days
        start_date = latest_entry.end_date
        end_date = start_date + timedelta(days=60)
    else:
        # If no data exists, fetch data from the last year
        start_date = timezone.now().date() - timedelta(days=365)
        end_date = start_date + timedelta(days=60)

    # Ensure end_date does not exceed the current date
    end_date = min(end_date, timezone.now().date())

    # Convert dates to LinkedIn API epoch format (milliseconds)
    start_timestamp = int(start_date.strftime('%s')) * 1000
    end_timestamp = int(end_date.strftime('%s')) * 1000

    # Define the API endpoint dynamically
    analytics_url = (
        f'{LINKEDIN_API_URL}/rest/organizationalEntityFollowerStatistics'
        f'?q=organizationalEntity'
        f'&organizationalEntity=urn:li:organization:13701784'
        f'&timeIntervals.timeGranularityType=DAY'
        f'&timeIntervals.timeRange.start={start_timestamp}'
        f'&timeIntervals.timeRange.end={end_timestamp}'
    )

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'LinkedIn-Version': LINKEDIN_APP_VERSION,
    }

    # Retrieve data from LinkedIn API
    response = requests.get(analytics_url, headers=headers)
    if response.status_code != 200:
        raise Exception(f'Error fetching data from LinkedIn API: {response.status_code} - {response.text}')
    
    analytics_data = response.json()

    # Iterate over the data and insert into the database
    for element in analytics_data.get('elements', []):
        if 'followerGains' in element:
            time_range_start = datetime.fromtimestamp(element['timeRange']['start'] / 1000)
            time_range_end = datetime.fromtimestamp(element['timeRange']['end'] / 1000)
            organic_follower_gain = element['followerGains'].get('organicFollowerGain')
            paid_follower_gain = element['followerGains'].get('paidFollowerGain')
            organizational_entity = element.get('organizationalEntity')

            # Prepare data for creation
            data = {
                'start_date': time_range_start.date(),
                'end_date': time_range_end.date(),
                'organic_follower_gain': organic_follower_gain,
                'paid_follower_gain': paid_follower_gain,
                'organizational_entity': organizational_entity,
                'user': user
            }

            # Create and save the new record
            LinkedinFollowersGainStatistics.objects.create(**data)