#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tweepy
import settings
import csv
import sys
import os
import urllib.request
import urllib.error

# コマンドライン引数が足りなければ終了
if len(sys.argv) < 2:
    print("使用法： python make_card.py 参加者データ [大会名] [開催地] [……]")
    print("例： python make_card.py data.csv 第1回大会")
    sys.exit()

#Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

#TwiiterIDの載ったCSVファイルの読み込み
csvfile = sys.argv[1]
reader_list = []
id_list = []
no_id_line = []
no_id_list = []
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
line_num = 1
icon_num = 1
for id in id_list:
    if '@' in id:
        id = id.lstrip('@')
    if '＠' in id:
        id = id.lstrip('＠')
    print(str(icon_num) + ':' + id)
    try:
        user = api.get_user(id)
    except tweepy.error.TweepError:
        print(str(line_num) + "行目の画像取得に失敗")
        no_id_line.append(line_num)
        line_num += 1
        continue
    url = user.profile_image_url_https.replace("_normal.", ".")
    other,ext = os.path.splitext(url)
    if not ext:
        ext = ".jpg"
    path = "./icon/" + str(icon_num) + ext
    try:
        data = urllib.request.urlopen(url).read()
        with open(path, mode="wb") as f:
            f.write(data)
    except urllib.error.URLError as e:
        print(e)
    line_num += 1
    icon_num += 1
print("アイコン画像の取得完了")

#input.csvを出力
if len(sys.argv) > 2:
    for i in range(2, len(sys.argv)):
        for j in range(0, len(reader_list)):
            reader_list[j].append(sys.argv[i])
if len(no_id_line) > 0:
    no_id_list.append(reader_list[0])
    for i in no_id_line:
        no_id_list.append(reader_list.pop(i))
        for j in range(0, len(no_id_line)):
            no_id_line[j] -= 1;
with open("./input.csv", 'w') as f:
    writer = csv.writer(f)
    writer.writerows(reader_list)
print("input.csvの出力完了")
if len(no_id_list) > 0:
    with open("./no_icon.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(no_id_list)
    print("アイコン画像を取得できなかった行をno_icon.csvとして出力しました")
