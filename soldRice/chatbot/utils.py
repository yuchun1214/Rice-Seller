import os
import yaml
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, ButtonsTemplate, PostbackAction, MessageAction

# print(os.path.dirname(__file__))

config_path = os.path.join(os.path.dirname(__file__),'config.yaml')
# print(config_path)

with open(config_path, 'r') as f:
    data = yaml.load(f)
    CHANNEL_SECRET = data['CHANNEL_SECRET']
    ACCESS_TOKEN = data['ACCESS_TOKEN']
    f.close()


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
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
                            "label":"是",
                            "text":"是"
                        },
                        {
                            "type":"message",
                            "label":"否",
                            "text":"否"
                        }
                    ])
                ))
 
    return "ok" 

def send_buttom_message(reply_token, title, text, options):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    line_bot_api.reply_message(reply_token,TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title=title,
            text=text,
            actions=options
            
        )))
    return 'ok'
