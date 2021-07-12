#!/bin/env python
import setting as s
from line.downloader import Worker
from line.messenger import reply_message
from action.messenger import act_reply_message
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage

# アプリケーションフレームワーク
app = Flask(__name__)

# LINE チャンネルシークレット
LINE_CHANNEL_SECRET = s.LINE_CHANNEL_SECRET
# LINE アクセストークン
LINE_CHANNEL_ACCESS_TOKEN = s.LINE_CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # X-Line-Signature シグネチャの取得
    signature = request.headers['X-Line-Signature']

    # 内容の取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # ウェブフックの確立
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=(TextMessage))
def line(event):
    # LINEメッセージイベント
    message = event.message.text
    try:
        get_id = event.source.group_id
    except AttributeError:
        get_id = event.source.user_id

    tag = message.split()[0]
    param = set(["/mp3","/mov","/nomov"])
    if tag in str(param) and message.startswith(tag):
        url = message.split()[1]
        err = reply_message(event,tag,url,line_bot_api)
        if err == None:
            Worker(tag,url,get_id,line_bot_api).run()
    else:
        act_reply_message(event,get_id,message,line_bot_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9000")