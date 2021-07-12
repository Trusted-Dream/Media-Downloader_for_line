# Media Downloader for LINE

![python](https://img.shields.io/badge/Python-3.9+-skyblue?style=plastic&logo=python)
![docker-compose-v3](https://img.shields.io/badge/docker_compose-v3-blue?style=plastic&logo=docker)
![tool-version](https://img.shields.io/badge/tool-v1.0.7-darkred?style=plastic&logo=pastebin)

## ツールについて
- LINEからYoutube,tiktok,soundcloud,Twitter,dailymotion,ニコニコ動画から音楽・動画のダウンロードに対応しています。<p>
- ダウンロード後は自動的に、変換→GoogleDriveにアップロード→LINEに完了通知を行います。
- Youtubeのプレイリストにも対応しています。
- 複数の音楽・動画の同時変換に対応し、GoogleDriveへの同時アップロードが行えます。(デフォルト4つ同時処理)

## 前提条件
- [LINE API](https://developers.line.biz/console/)を取得してください。
- [GoogleDriveAPI](https://console.developers.google.com/apis/library/drive.googleapis.com)を取得してください。
- docker-composeを準備してください。<p>
※環境が汚れますが、python3.9を導入してpip install後にapp.pyを叩いても動作します。
- [ngrok](https://ngrok.com/)を準備してください。

## 準備
- [Google Developers Console](https://console.developers.google.com/) にアクセスしてOAuth 2.0 クライアント ID からclient_secrets.jsonを取得します。<p>
https://console.developers.google.com/<p>
`client_secrets.json`に名前を変更し、`credentials`ディレクトリに設置します。
- `settings_sample.yaml`を`settings.yaml`に変更し、`xxxx`の部分にGoogleOAuthの情報を記入します。
- `.env.sample` を参考に`.env`を作成します。<p>
(GoogleDriveの共有IDは `https://drive.google.com/drive/u/0/folders/` 以降の英数字を記入します。)
- `docker-compose build`を実行してビルドします。
- `docker-compose run --rm app`を実行して認証します。
- バックグラウンドで実行させる場合は、Ctrl + Cで一旦停止後、`docker-compose up -d` で起動します。<p>
　※認証後は `docker-compose up -d` で起動できます。
- ngrokを起動し`ngrok http -region=ap 9000` を実行します。
- httpsから始まるURLをLINEの`Webhook URL`に末尾に`/callback`を追加して入力します。<p>
  <例> `https://2aeebc8adb35.ap.ngrok.io/callback`
- LINEアプリから`!test` と入力してレスポンスがあれば完了です。
## 使用方法
- `docker-compose up -d`を実行<p>
- ngrokを起動して`ngrok http -region=ap 9000` で起動
- [LINE developers](https://developers.line.biz/console/)にアクセスして、Webhook設定の検証でステータスコード200が返ることを確認してください。
- LINE から以下のようにコマンドを入力させて動作します。
- /mp3 URL -- 音楽を取得できます。
- /mov URL -- 動画を取得できます。
- /nomov URL -- 動画を無変換で取得できます。