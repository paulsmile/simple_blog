#coding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str, smart_unicode
from weixin.models import WeixinClientUser
from django.conf import settings

RES_TEXT_FORMAT = '''
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>'''


@csrf_exempt
def weixin_api(request):
    '''API interface of the weixin MP.'''

    import logging
    if not request.GET and not request.body:
        return HttpResponse()

    confirm = checkSignature(request)
    if request.method == 'GET':
        return HttpResponse(confirm)
    elif request.method == 'POST':
        if confirm:
            ###
            resMsg = paraseMsg(request)
            return HttpResponse(resMsg)
        else:
            logging.warning('weixin sign fail!')
            return HttpResponse('')


def checkSignature(request):
    '''Checking the messages to confirm whether they are come from weixin MP.'''

    import hashlib
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echoStr = request.GET.get('echostr', None)
    token = settings.TOKEN
    tmpArr = ''.join(sorted([token, timestamp, nonce]))
    tmpArr = hashlib.sha1(tmpArr).hexdigest()

    if tmpArr == signature:
        return echoStr
    else:
        return False


def paraseMsg(request):
    '''Handling the requests from weixin MP which are sending by 'POST' method.'''
    import xml.etree.ElementTree as ET
    rawStr = request.raw_post_data
    msg = paraseMsgXml(ET.fromstring(rawStr))
    if 'Event' in msg:
        return paraseEvent(msg)
    if 'Content' in msg:
        return responeCliMsg(msg)


def paraseMsgXml(root_elem):
    '''Change XML to dict.'''
    msg = {}
    if root_elem.tag == 'xml':
        for child in root_elem:
            msg[child.tag] = smart_str(child.text)
    return msg


def paraseEvent(msg):
    '''Handling the events which are send from weixin MP by 'POST' method.'''
    # msg is a dict
    if msg['Event'] == 'subscribe':
        weixinClientUser = WeixinClientUser(UserName=msg['FromUserName'])
        weixinClientUser.save()
        return sendMsg('text', msg['FromUserName'],
            Content = 'Hello, 您已经成功订阅了此公众平台',
        )
    elif msg['Event'] == 'SCAN':
        return sendMsg('text', msg['FromUserName'],
            Content = 'Hello, 您之前已经成功订阅过此公众平台了',
        )


def responeCliMsg(msg):
    '''Respone the client's messages.'''
    return sendMsg('text', msg['FromUserName'],
        Content = 'Hello, 收到您的信息啦',
    )


def sendMsg(type, client_user, **msg):
    '''Change the messages into XML format.'''
    import time
    if type == 'text':
        ToUserName = settings.ToUserName
        FromUserName = client_user
        CreateTime = int(time.time())
        MsgType = 'text'
        Content = msg['Content']
        return RES_TEXT_FORMAT % (ToUserName, FromUserName, CreateTime,
            MsgType, Content)

    else:
        pass
