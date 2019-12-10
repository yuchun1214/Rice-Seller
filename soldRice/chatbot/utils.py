import os
import re
import yaml
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from linebot import LineBotApi
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, ButtonsTemplate, PostbackAction, MessageAction, ImageSendMessage

# print(os.path.dirname(__file__))

config_path = os.path.join(os.path.dirname(__file__),'config.yaml')
mail_message = os.path.join(os.path.dirname(__file__), 'mail.html')
# print(config_path)

with open(config_path, 'r') as f:
    data = yaml.load(f)
    CHANNEL_SECRET = data['CHANNEL_SECRET']
    ACCESS_TOKEN = data['ACCESS_TOKEN']
    PASSWORD = data['PASSWORD']
    f.close()

with open(mail_message, 'r') as f:
    mail = f.read()
    f.close()


class orderMail(object):
    def __init__(self):
        self.sender = "e64061151@gs.ncku.edu.tw"
        self.server = smtplib.SMTP("smtp.gmail.com", 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.sender, PASSWORD)
        self.server.ehlo()
        self.receiver_email = 'yuchunlin0075@gmail.com'
        self.msg = EmailMessage()
                

    def set_content(self, content):
        
        message = re.sub(r'xxx', content, mail)
        msg = MIMEText(message, 'html', 'utf8')
        msg["Subject"] = "[NEW]Order"
        msg["From"] = self.sender
        msg["To"] = self.receiver_email 
        self.msg = msg.as_string()
        
    
    def sending(self):
        self.server.sendmail(self.sender, self.receiver_email, self.msg)

    def quit(self):
        self.server.quit()


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

def send_fsm_graph(reply_token):
    line_bot_api = LineBotApi(ACCESS_TOKEN)
    line_bot_api.reply_message(reply_token, ImageSendMessage(
        original_content_url='https://bdeb2c01.ngrok.io/static/graph.png',
        preview_image_url = 'https://bdeb2c01.ngrok.io/static/graph.png'
    ))
if __name__ == '__main__':
    pass
