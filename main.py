# -*- coding: utf-8 -*-
import json
import urllib.parse as urlparse
import urllib
import requests
import sqlite3
import contextlib

NICO_CONTENTS_SEARCH_API_END_POINT = "http://api.search.nicovideo.jp/api/v2/video/contents/search"

DB_PATH = "env/kitchen_db.db"

def search_voiro_kitchen_hijiki(*keywords):
    search_keywords = "VOICEROIDキッチン"
    if len(convert_tuple_to_str(keywords)) > 0:
        search_keywords = convert_tuple_to_str(keywords)

    search_url = NICO_CONTENTS_SEARCH_API_END_POINT
    search_url += "?q=" + urlparse.quote(search_keywords)
    search_url += "&targets=tagsExact"
    search_url += "&_limit=100"
    search_url += "&_sort=-viewCounter"
    search_url += "&_context=apitest"
    search_url += "&fields=contentId,title,description,tags,categoryTags,viewCounter,mylistCounter,commentCounter,startTime,lastCommentTime,lengthSeconds"

    r = requests.get(search_url)
    req_json = json.dumps(r.json(),ensure_ascii=False)
    req_json_dict = json.loads(req_json)

    return req_json_dict

def convert_tuple_to_str(tpl):
    search_keywords = ""
    if len(tpl) > 0:
        for word in tpl:
            search_keywords += str(word) + " "
        search_keywords.rstrip()
    return search_keywords

def insert_json_data(json_dict):
    with contextlib.closing(sqlite3.connect(DB_PATH)) as con:
        cur = con.cursor()

        create_sql = "create table if not exists SERCH_NICO_VIDEO ( \
                    CREATE_DATE text not null \
                    , CONTENT_ID text not null \
                    , TITLE text not null \
                    , TAGS text \
                    , CATEGORY_TAG text not null \
                    , VIEW_CNT numeric not null \
                    , MYLIST_CNT numeric not null \
                    , COMMENT_CNT numeric not null \
                    , START_DATE text not null \
                    , LENGTH_SEC numeric \
                    , LAST_COMMENT_TIME text \
                    , DISCRIPTION text \
                    , constraint SERCH_NICO_VIDEO_PKC primary key (CREATE_DATE,CONTENT_ID) \
                    ) ;"

        cur.execute(create_sql)

        ins_sql = "INSERT \
                    INTO SERCH_NICO_VIDEO( \
                    CREATE_DATE \
                    , CONTENT_ID \
                    , TITLE \
                    , TAGS \
                    , CATEGORY_TAG \
                    , VIEW_CNT \
                    , MYLIST_CNT \
                    , COMMENT_CNT \
                    , START_DATE \
                    , LENGTH_SEC \
                    , LAST_COMMENT_TIME \
                    , DISCRIPTION \
                    ) VALUES (datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        for data in json_dict["data"]:
            # contentId,title,description,tags,categoryTags,
            # viewCounter,mylistCounter,commentCounter,
            # startTime,lastCommentTime,lengthSeconds
            contentid = str(data["contentId"])
            title = str(data["title"])
            descr = str(data["description"])
            tags = str(data["tags"])
            cat_tag = str(data["categoryTags"])
            viewCnt = str(data["viewCounter"])
            myListCnt = str(data["mylistCounter"])
            commentCnt = str(data["commentCounter"])
            startTime = str(data["startTime"])
            lastCmtTime = str(data["lastCommentTime"])
            lenSec = str(data["lengthSeconds"])

            params = [contentid, title, tags, cat_tag, viewCnt, \
            myListCnt, commentCnt, startTime, lenSec, lastCmtTime ,descr]
            #print(contentid + "," + title + "," + viewCnt + "," + myListCnt + "," + commentCnt + "," + startTime)

            cur.execute(ins_sql, params)

        con.commit()

if __name__ == "__main__":
    data = search_voiro_kitchen_hijiki("VOICEROIDキッチン", "第四回ひじき祭")
    insert_json_data(data)