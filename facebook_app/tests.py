# from django.test import TestCase

# Create your tests here.
import os
import requests
client_id = os.getenv('FB_CLIENT_ID')  # Your Facebook App ID
client_secret =  os.getenv('FB_CLIENT_SECRET')
redirect_uri = os.getenv('FB_REDIRECT_URL')  # Your redirect URI without email

# Step 3: Exchange the authorization code for an access token
token_url = "https://graph.facebook.com/v22.0/oauth/access_token"
params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "client_secret": client_secret,
    "code": 'AQBtQAnICb-D_LuZFFqltJCjiMMokQ7pk6Iy-LMAIX9ULOmNiLd3sBq06kywVTwxAepJO7Yw6W-_lyQ7F_D8oY2qeJn5si12qbU9GRPXGykNe9OCwDBqMhx2lofrZx7iV1c6j5DVpMydRz561rsouoK0SSOGxHLlI_uHNL_5X-KgptvbOZthDyhiCyqUDyCQzMEkagS6LzZxWXyb7L7xQRv3aFlgBs0HeoP8wCfRKg3Rv0F2IzJ9edJnwLxp5Qw8DpIeXOqN7iuGzbRcW3EmaayrxCq2a7WtHkpJeYjY5glK9MUml5hcxgc2eSmBwetueMLrLaGFsbGjCFS52-c9NGBMXw5OBfOLQWqjcQ8K5n1HlEcE9Cof3f8C1Gih-zilGvM',
}

response = requests.get(token_url, params=params)
response_data = response.json()
print(response.text)
print(response_data)