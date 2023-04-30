## ■ 技術仕様

- Backend: Python（Version: 3.11.3）
- Database: Notion API  
→ https://developers.notion.com
- Infrastructure: Cloudfrare R2

## ■ 機能仕様

### ① YouTube 動画ダウンロード機能

```Python
import json
import os
import requests
import subprocess

from datetime import date
from yt_dlp import YoutubeDL

class YouTubeVideo:
  def __init__(self, id, category, channel_name, title, thumbnail_url, upload_date, duration):
    self.id: str = id
    self.category: str = category
    self.channel_name: str = channel_name
    self.title: str = title
    self.thumbnail_url: str = thumbnail_url
    self.upload_date: date = upload_date
    self.duration: int = duration

# ▼ サムネイル画像一覧の中から、最も大きいサイズを抽出 ▼
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

    headers = {
      'accept': 'application/json',
      'content-type': 'application/json',
      'Notion-Version': '2022-06-28',
      'Authorization': f"Bearer {os.getenv('NOTION_API_TOKEN')}"
    },

    # NotionAPI プロパティ記述方法: https://www.6666666.jp/productivity/20210617
    json = {
      'parent': {'database_id': os.getenv('NOTION_DATABASE_ID')},
      'cover': {
        'type': 'external',
        'external': {'url': youtube_video.thumbnail_url}
      },
      'properties': {
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
          'url': youtube_video.thumbnail_url
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

video_id_list = ['', '', ''] # ダウンロードする動画の Video_ID
for video_id in video_id_list:
  video_info = YoutubeDL().extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
  # ▼ 必要項目 取得 ▼
  youtube_video = YouTubeVideo(
    video_info['id'], # Video_ID
    video_info['categories'][0],  # カテゴリー名
    video_info['channel'],  # チャンネル名
    video_info['title'],  # 動画タイトル
    get_thumbnail_url(video_info),  # サムネイル画像
    date(int(video_info['upload_date'][0:4]), int(video_info['upload_date'][4:6]), int(video_info['upload_date'][6:8])),  # 動画公開日
    video_info['duration']  # 再生時間
  )

  # ▼ FullHD（.mkv）でダウンロード ▼
  subprocess.run(["yt-dlp", "--format-sort", "res:1080", "--merge-output-format", "mkv/mp4", f"https://www.youtube.com/watch?v={video_id}"])
  create_notion_page(youtube_video) # NotionDB にレコード登録
```
