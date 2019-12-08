import os
import yaml
import json
from . import fsm, utils
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, PostbackAction, MessageAction
from django.conf import settings

line_bot_api = LineBotApi(settings.ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)
parser = WebhookParser(settings.CHANNEL_SECRET)



print("os.path.dirname = ",os.path.dirname(__file__))

def index(request):
    print("line_bot_api : ",line_bot_api)
    return HttpResponse("Hello, world. You're at the index.")

@csrf_exempt
def testing(request):
    body = request.body.decode('utf-8')
    print(body)
    return HttpResponse('ok')

@csrf_exempt
def callback(request):
    signature = request.headers['X-Line-Signature']
    body = request.body.decode('utf-8')
    json_body = json.loads(body)
    print(json.dumps(json_body,indent=4))
   
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        print("Signature : ", signature,end='\n\n')
        print("access token : ",settings.ACCESS_TOKEN,end='\n\n')
        print("channel_secret", settings.CHANNEL_SECRET,end='\n\n')
        print("Invalid signature, Please check your access token/channel secret.")

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
    
        utils.send_confirm_message(event.reply_token,"Are you Ok" )

    return HttpResponse("Ok")


# Create your views here.
