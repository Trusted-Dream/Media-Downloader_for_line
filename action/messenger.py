from linebot.models import TextSendMessage
def act_reply_message(event,get_id,message,line_bot_api):
    if message.startswith("!test"):
        m = [TextSendMessage(text="1回目")]
        m.append(TextSendMessage(text="2回目"))
        m.append(TextSendMessage(text="3回目"))
        line_bot_api.reply_message(event.reply_token,m)