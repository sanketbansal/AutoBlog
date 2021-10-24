import requests
import json, base64, re
from datetime import datetime

access_token = ''
site_id = 176416011

def authenticate():
    auth = {
        'client_id': '77453',
        'client_secret': '7b9RDuBX8kaLWQ2bt7d2EsSJGOww7BVDSQx3KdzNbP9bUYI4i4gU3kW0YAMMUk5G',
        'grant_type': 'password',
        'username': 'sanketbansal57',
        'password': 'sank@1902',
    }

    # auth = {
    #     'client_id': '77453',
    #     'client_secret': '7b9RDuBX8kaLWQ2bt7d2EsSJGOww7BVDSQx3KdzNbP9bUYI4i4gU3kW0YAMMUk5G',
    #     'redirect_uri': 'https://lavizz.com/',
    #     'code': 'EBPXZHip3A',
    #     'grant_type':'authorization_code'
    # }

    response = requests.post('https://public-api.wordpress.com/oauth2/token', data=auth).json()
    print(response, '\n')
    access_token = response['access_token']

    # site_id = 176416011 // LAVIZ


def create_post(title, content, tags = [], categories = []):
    params = {
        'date_gmt': datetime.now().replace(microsecond=0).isoformat() + "Z",
        'status': 'draft',
        'title': title,
        'content': content,
        'tags': tags,
        'categories': categories
    }

    if(access_token == ''):
        print("Authenticating....", '\n')
        authenticate()

    header = {'Authorization': 'Bearer ' + access_token}

    wordpress_url = 'https://public-api.wordpress.com/rest/v1.2/sites/' + site_id + '/posts/new/'
    response = requests.post(wordpress_url, headers=header, data=params)

    print("Posting....", '\n')
    print(response.json(), '\n')

