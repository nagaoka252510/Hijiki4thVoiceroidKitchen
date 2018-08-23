# -*- coding: utf-8 -*-
import json
import urllib.parse as urlparse
import urllib
import requests

NICO_CONTENTS_SEARCH_API_END_POINT = "http://api.search.nicovideo.jp/api/v2/video/contents/search"

def search_voiro_kitchen_hijiki():
    # TODO APIを叩くURLの生成は別クラスにまとめたい
    search_url = NICO_CONTENTS_SEARCH_API_END_POINT
    search_url += "?q=" + urlparse.quote("VOICEROIDキッチン 第四回ひじき祭")
    search_url += "&targets=tagsExact"
    search_url += "&_limit=100"
    search_url += "&_sort=-startTime"
    search_url += "&_context=apitest"
    search_url += "&fields=contentId,title,description,tags,categoryTags,viewCounter,mylistCounter,commentCounter,startTime,lastCommentTime,lengthSeconds"

    #print(search_url)

    r = requests.get(search_url)
    req_json = json.dumps(r.json(),ensure_ascii=False)
    req_json_dict = json.loads(req_json)

    return req_json_dict

def insert_json_data(json_dict):
    for data in json_dict["data"]:
        print(data["contentId"])

if __name__ == "__main__":
    data = search_voiro_kitchen_hijiki()
    insert_json_data(data)