#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import settings
import csv
import sys
import os
import urllib.request
import urllib.error

#Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#TwiiterIDの載ったCSVファイルの読み込み
print("CSVファイルの名前を入力してください")
csvfile = input()
reader_list = []
id_list = []
with open(csvfile,'r') as f:
    reader_list = list(csv.reader(f))
    id_row = 0
    is_ID_exist = False
    #TwitterIDの書かれた列を探す
    for head in reader_list[0]:
        if ("Twitter" in head or "twitter" in head) and "ID" in head:
            is_ID_exist = True
            break;
        id_row += 1
    if not is_ID_exist:
        sys.exit("TwitterIDが見つかりません")
    #TwitterIDの書かれた列の中身をid_listにコピー
    for i in range(1, len(reader_list)):
        id_list.append(reader_list[i][id_row])

#アイコン画像を取得しiconディレクトリに格納
try:
    os.mkdir("./icon")
except FileExistsError as e:
    print("Error!")
    print(e)
    print("ファイル\'icon\'が既に存在します。削除してください。")
    sys.exit()

print("アイコン画像の取得を開始")
icon_num = 1
for id in id_list:
    if '@' in id:
        id = id.lstrip('@')
    print(str(icon_num) + ':' + id)
    user = api.get_user(id)
    url = user.profile_image_url_https.replace("_normal.", ".")
    other,ext = = os.path.splitext(url)
    if not ext:
        ext = ".jpg"
    path = "./icon/" + str(icon_num) + ext
    try:
        data = urllib.request.urlopen(url).read()
        with open(path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)
    icon_num += 1
print("アイコン画像の取得完了")

#input.csvを出力
print("大会名を入力してください")
tour_name = input()
reader_list[0].append("大会名")
for i in range(1, len(reader_list)):
    reader_list[i].append(tour_name)
with open("./input.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerows(reader_list)
print("input.csvの出力完了")
