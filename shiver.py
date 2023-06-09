import json
import os

import requests
from moviepy.editor import CompositeVideoClip, VideoFileClip
from requests.models import PreparedRequest

twitch_auth_url = 'https://id.twitch.tv/oauth2/token'
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_client_secret = os.environ.get('TWITCH_CLIENT_SECRET')
# twitch_search_url = 'https://api.twitch.tv/helix/videos'
twitch_search_url = 'https://api.twitch.tv/helix/clips'

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


# started_at=2022-07-03T00:00:00Z&ended_at=2022-07-09T00:00:00Z

def get_latest_twitch_vod():
    twitch_token = get_twitch_token()
    # params = {'user_id': '21841789', 'type': 'archive'}
    params = {'broadcaster_id': '21841789',
              'type': 'archive', 'started_at': '2023-03-03T00:00:00Z', 'ended_at': '2023-03-09T00:00:00Z'}
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
    print('🚀 New twitch vod! pog! 🚀')

    twitch_vod_id = latest_twitch_vod['data'][0]['id']
    # p = subprocess.Popen('./TwitchDownloaderCLI videodownload --id {0} --ffmpeg-path "ffmpeg.exe" -o {0}.mp4'.format(twitch_vod_id),
    #                      stdout=subprocess.PIPE, shell=True)
    os.system(
        './TwitchDownloaderCLI clipdownload --id {} -o ./vods/clip.mp4'.format(twitch_vod_id))
    os.system(
        './TwitchDownloaderCLI chatdownload --id {} -o ./chats/chat.json -E'.format(twitch_vod_id))
    os.system(
        './TwitchDownloaderCLI chatrender -i ./chats/chat.json -h 360 -w 422 --generate-mask true --font-size 18 --background-color "#00000000" -o ./chats/chat.mp4'.format(twitch_vod_id))

    chat_mask_clip = VideoFileClip('./chats/chat_mask.mp4')
    chat_mask_clip.ismask = True
    chat_clip = VideoFileClip('./chats/chat.mp4')
    chat_clip.set_mask(chat_mask_clip)

    # chat_video = CompositeVideoClip([chat_clip, chat_mask_clip])
    # chat_video.write_videofile('./chats/masked_chat.mp4')

    # masked_chat_clip = VideoFileClip('./chats/masked_chat.mp4')
    video_clip = VideoFileClip('./vods/clip.mp4')

    final_video = CompositeVideoClip([video_clip, chat_clip])
    final_video.write_videofile('overlay.mp4')

    print('✨ vod downloaded! ✨')
else:
    print('no new twitch vod :(')
