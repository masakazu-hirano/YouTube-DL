import json
import os
import requests
import subprocess

from datetime import date
from dotenv import load_dotenv
from Modules.GET_NotionDB_List import get_notion_list
from PIL import Image
from urllib.request import urlopen
from yt_dlp import YoutubeDL

class YouTubeVideo:
    def __init__(self, id, category, channel_name, title, thumbnail_url, upload_date, duration):
        self.id: str = id
        self.category: str = category
        self.channel_name: str = channel_name
        self.title: str = title
        self.thumbnails: str = thumbnail_url
        self.upload_date: date = upload_date
        self.duration: int = duration

def set_notion_header():
    return {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Notion-Version': '2022-06-28',
        'Authorization': f"Bearer {os.getenv('NOTION_API_TOKEN')}"
    }

def get_thumbnail_url(video_info):
    max_width = 0
    thumbnail_url = None
    for thumbnail in video_info['thumbnails']:
        try:
            if thumbnail['width'] > max_width:
                max_width = thumbnail['width']
                thumbnail_url = thumbnail['url']
        except KeyError:
            pass

    return thumbnail_url

def create_notion_page(youtube_video):
    return requests.post(
        'https://api.notion.com/v1/pages',
        headers = set_notion_header(),

        # NotionAPI プロパティ記述方法: https://www.6666666.jp/productivity/20210617
        json = {
            'parent': {'database_id': os.getenv('NOTION_DATABASE_ID')},
            'cover': {'external': {
                        'url': youtube_video.thumbnails
                      }}
            'properties':
            {
                'ID': {
                    'rich_text': [{
                        'text': {'content': youtube_video.id}
                    }]
                },

                'カテゴリー': {
                    'select': {
                        'name': youtube_video.category,
                        'color': 'gray'
                    }
                },

                'チャンネル名': {
                    'select': {
                        'name': youtube_video.channel_name,
                        'color': 'gray'
                    }
                },

                'タイトル': {
                    'title': [{
                        'text': {'content': youtube_video.title}
                    }]
                },

                'サムネイル画像': {
                  'url': youtube_video.thumbnails
                },

                '再生時間': {
                    'number': youtube_video.duration
                },

                '公開日': {
                    'date': {
                        'start': str(youtube_video.upload_date),
                        'end': None
                    }
                }
            }
        }
    )

if __name__ == '__main__':
    load_dotenv()

    video_id_list = ['YouTube_VideoID']
    index = 1
    for video_id in video_id_list:
        already_video_id_list = get_notion_list()
        if already_video_id in already_video_id_list:
            print(f'{already_video_id}: 既に登録されています。')
            index += 1
            continue

        video_info = YoutubeDL().extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
        youtube_video = YouTubeVideo(
            video_info['id'],
            video_info['categories'][0],
            video_info['channel'],
            video_info['title'],
            get_thumbnail_url(video_info),
            date(int(video_info['upload_date'][0:4]), int(video_info['upload_date'][4:6]), int(video_info['upload_date'][6:8])),
            video_info['duration']
        )

        print(f'▼ 処理開始（{index}/{len(video_id_list)}）: {youtube_video.title} ▼')
        subprocess.run(["yt-dlp", "--format-sort", "res:1080", "--merge-output-format", "mkv/mp4", f"https://www.youtube.com/watch?v={video_id}"])
            # YouTube動画を、FullHD（.mkv）でダウンロード
        print(f'ダウンロード完了: {youtube_video.title}')

        response = create_notion_page(youtube_video)
        if response.status_code == 200:
            print(f"NotionDB 登録完了: {json.loads(response.text)['id']}")
        else:
            print(f'NotionDB 登録失敗: {youtube_video.id}')

        print('------------------------------')
        index += 1
    print('処理が正常終了しました。')
