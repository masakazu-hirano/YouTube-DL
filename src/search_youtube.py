import os

from apiclient.discovery import build

if __name__ == '__main__':
    authorize_youtube = build('youtube', 'v3', developerKey = f"{os.getenv('youtube_token')}")

    # https://developers.google.com/youtube/v3/docs/search/list
    response = authorize_youtube.search().list(
        part = 'id, snippet',
        channelType = 'any',
        q = '検索キーワード',
        order = 'relevance',
        safeSearch = 'none',
        maxResults = 50,
    ).execute()

    print(response)
