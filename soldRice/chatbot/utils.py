import os
import yaml
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction

# print(os.path.dirname(__file__))

config_path = os.path.join(os.path.dirname(__file__),'config.yaml')
# print(config_path)

with open(config_path, 'r') as f:
    data = yaml.load(f)
    CHANNEL_SECRET = data['CHANNEL_SECRET']
    ACCESS_TOKEN = data['ACCESS_TOKEN']
    f.close()


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi()
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "ok"

def send_confirm_message(reply_token, text):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    line_bot_api.reply_message(
            reply_token,TemplateSendMessage(
                alt_text='Confirm template',
                template=ConfirmTemplate(
                    text=text,
                    actions=[
                        {
                            "type":"message",
                            "label":"yes",
                            "text":"yes"
                        },
                        {
                            "type":"message",
                            "label":"no",
                            "text":"no"
                        }
                    ])
                ))
 
    return "ok" 
