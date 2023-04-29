import json
import os
import requests

from dotenv import load_dotenv

def set_notion_header():
    return {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Notion-Version': '2022-06-28',
        'Authorization': f"Bearer {os.getenv('NOTION_API_TOKEN')}"
    }

def get_notion_list():
    load_dotenv()

    loop_count = 0
    has_more = True
    results = []
    while has_more:
        if loop_count == 0:
            video_id_list = requests.post(
                f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}/query",
                headers = set_notion_header(),
                json = {'page_size': 100} # 取得件数の上限は100件
            ).text
        elif loop_count > 0:
            video_id_list = requests.post(
                f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}/query",
                headers = set_notion_header(),
                json = {
                    'start_cursor': start_cursor,
                    'page_size': 100 # 取得件数の上限は100件
                }
            ).text

        # TODO: ここに値を取得する処理を実装

        if json.loads(video_id_list)['has_more']: # Request（'page_size'） 以上の件数が取得された場合、'has_more' プロパティに True が返る。
            start_cursor = json.loads(video_id_list)['next_cursor']
        else:
            has_more = json.loads(video_id_list)['has_more']
                # 'has_more' プロパティが False の場合、ループを終了

        loop_count += 1

    # TODO: ここに返却する Return を記述
    # NotionDB プロパティの取得先
        # ページID: json.loads(response.text)['results']['id']
        # プロパティ: json.loads(response.text)['results']['properties']['プロパティ名']
