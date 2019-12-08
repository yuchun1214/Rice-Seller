import os
import yaml
import json
from . import fsm
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from django.conf import settings

line_bot_api = LineBotApi(settings.ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)


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
        handler.handle(body,signature)
    except InvalidSignatureError:
        print("Signature : ", signature,end='\n\n')
        print("access token : ",settings.ACCESS_TOKEN,end='\n\n')
        print("channel_secret", settings.CHANNEL_SECRET,end='\n\n')
        print("Invalid signature, Please check your access token/channel secret.")
    return HttpResponse("Ok")

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="學屁學喔"))


# Create your views here.
