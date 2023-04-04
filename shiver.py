import json
import os

import requests
from requests.models import PreparedRequest

twitch_auth_url = 'https://id.twitch.tv/oauth2/token'
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
twitch_search_url = 'https://api.twitch.tv/helix/videos'

youtube_search_url = 'https://youtube.googleapis.com/youtube/v3/search'
youtube_key = os.environ.get('YOUTUBE_KEY')


def get_twitch_token():
    response = requests.post(
        twitch_auth_url,
        data={'client_id': twitch_client_id, 'client_secret': twitch_client_secret,
              'grant_type': 'client_credentials'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    json_response = json.loads(response.text)
    return json_response['access_token']


def get_latest_twitch_vod():
    twitch_token = get_twitch_token()
    params = {'user_id': '21841789', 'type': 'archive'}
    req = PreparedRequest()
    req.prepare_url(twitch_search_url, params)
    response = requests.get(req.url, headers={
                            'Client-Id': twitch_client_id, 'Authorization': 'Bearer {}'.format(twitch_token)})
    json_response = json.loads(response.text)
    return json_response


def get_latest_youtube_vod():
    params = {'part': 'snippet', 'channelId': 'UCyclX6ZQCOXunEg4Z7EA8fw',
              'maxResults': '1', 'order': 'date', 'key': youtube_key}
    req = PreparedRequest()
    req.prepare_url(youtube_search_url, params)
    response = requests.get(req.url)
    return json.loads(response.text)


latest_twitch_vod = get_latest_twitch_vod()
latest_twitch_title = latest_twitch_vod['data'][0]['title']

latest_youtube_vod = get_latest_youtube_vod()
latest_youtube_title = latest_youtube_vod['items'][0]['snippet']['title']

if (latest_twitch_title != latest_youtube_title):
    print('New twitch vod! pog!')
