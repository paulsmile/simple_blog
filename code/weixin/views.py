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
    '''微信公众平台接口，负责响应公众平台发送过来的所有消息'''
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
    '''验证所收到的信息是否来自微信公众平台'''
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
    '''处理微信公众平台所有以POST方式传过来的数据'''
    import xml.etree.ElementTree as ET
    rawStr = request.raw_post_data
    msg = paraseMsgXml(ET.fromstring(rawStr))
    if 'Event' in msg:
        return paraseEvent(msg)
    if 'Content' in msg:
        return responeCliMsg(msg)


def paraseMsgXml(root_elem):
    '''把XML格式的文件转换为字典'''
    msg = {}
    if root_elem.tag == 'xml':
        for child in root_elem:
            msg[child.tag] = smart_str(child.text)
    return msg


def paraseEvent(msg):
    '''当公众平台POST过来的信息是事件类型时，处理该事件'''
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
    '''回应客户发送过来的信息'''
    return sendMsg('text', msg['FromUserName'],
        Content = 'Hello, 收到您的信息啦',
    )


def sendMsg(type, client_user, **msg):
    '''把需要发送的内容转化为xml格式'''
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
