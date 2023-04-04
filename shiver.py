import json
import os

import requests
from requests.models import PreparedRequest

client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')

auth_url = 'https://id.twitch.tv/oauth2/token'
videos_url = 'https://api.twitch.tv/helix/videos'

youtube_search_url = 'https://youtube.googleapis.com/youtube/v3/search'
youtube_key = os.environ.get('YOUTUBE_KEY')


def get_oauth_token():
    response = requests.post(
        auth_url,
        data={'client_id': client_id, 'client_secret': client_secret,
              'grant_type': 'client_credentials'},
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    json_response = json.loads(response.text)
    return json_response['access_token']


def get_videos(token):
    params = {'user_id': '21841789', 'type': 'archive'}
    req = PreparedRequest()
    req.prepare_url(videos_url, params)
    response = requests.get(req.url, headers={
                            'Client-Id': client_id, 'Authorization': 'Bearer {}'.format(token)})
    json_response = json.loads(response.text)
    return json_response['data']


def get_current_videos():
    params = {'part': 'snippet', 'channelId': 'UCyclX6ZQCOXunEg4Z7EA8fw',
              'maxResults': '1', 'order': 'date', 'key': youtube_key}
    req = PreparedRequest()
    req.prepare_url(youtube_search_url, params)
    response = requests.get(req.url)
    return json.loads(response.text)


token = get_oauth_token()
videos = get_videos(token)
# print(videos[0])

latest_nmp = get_current_videos()
print(latest_nmp)

# get latest twitch vod
# get latest youtube vod
# if mismatch twitch download twitch vod
