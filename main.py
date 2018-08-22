# -*- coding: utf-8 -*-
import requests
import json
import urllib.parse as urlparse

NICO_CONTENTS_SEARCH_API_END_POINT = "http://api.search.nicovideo.jp/api/v2/video/contents/search"

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

# TODO sqlite3に情報を保存する
with open("./voiceroid_kitchen.txt","w",encoding="utf_8") as wf:
    wf.write(req_json)

#print(r)

#print(req_json)
