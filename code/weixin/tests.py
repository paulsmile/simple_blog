from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
import random
import time
import hashlib


class WeiXinMPAPITest(TestCase):

    #fixtures = []
    def setUp(self):
        self.url = reverse('weixin_api', )
        self.send_token = settings.TOKEN
        self.send_timestamp = str(int(time.time()))
        self.send_nonce = str(random.randint(0, 1000))
        self.send_tmpArr = ''.join(sorted([
            self.send_token,
            self.send_timestamp,
            self.send_nonce,
        ]))
        self.send_signature = hashlib.sha1(self.send_tmpArr).hexdigest()

    def test_check_signature(self):
        send_echostr = str(random.randint(0, 1000))
        send_msg = {
            'signature': self.send_signature,
            'timestamp': self.send_timestamp,
            'nonce': self.send_nonce,
            'echostr': send_echostr,
        }
        resp = self.client.get(self.url, send_msg)
        self.assertEqual(resp.content, send_echostr)
