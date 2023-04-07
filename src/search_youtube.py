import os

from apiclient.discovery import build

if __name__ == '__main__':
    authorize_youtube = build('youtube', 'v3', developerKey = f"{os.getenv('youtube_token')}")

    # https://developers.google.com/youtube/v3/docs/search/list
    response = authorize_youtube.search().list(
        part = 'id, snippet',
        regionCode = 'JP',
        channelType = 'any',
        q = '検索キーワード',
        order = 'relevance',
        safeSearch = 'none',
        maxResults = 50,
    ).execute()

    video_lists = []
    for video in response['items']:
        video_lists.append(
            {
                'チャンネルID': video['snippet']['channelId'],
                'チャンネル名': video['snippet']['channelTitle'],
                'ID': video['id']['videoId'],
                'タイトル': video['snippet']['title'],
                '公開日': video['snippet']['publishTime'],
                'サムネイル画像URL': video['snippet']['thumbnails']['high']['url']
            }
        )

    print(video_lists)
