# make_card

大会参加者に配布するTwitterアイコン入り名刺をラベル屋さんで作成するためのプログラム

##Description
1.参加者情報の載ったcsvファイルを読み込む
2.TwitterIDを取り出し、TwitterAPIを叩いて対応するアイコン画像をダウンロード
3.csvファイルを整えてinput.csvとして出力

##Requirement
*TwitterAPIキーの取得
*Python3の使用環境
*Tweepyのインストール

##Usage
1.make_card.pyを実行
2.同じフォルダにアイコン画像の入ったiconフォルダと入力用ファイルinput.csvが作成される
3.ラベル屋さんの差し込み印刷を使用してinput.csvを読み込む
4.画像ファイルは番号順の名前になっているので「連番作成」で読み込める
