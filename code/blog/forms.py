#! /usr/bin/env python
#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django_comments.forms import CommentForm

import re

'''
class RegistrationForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=30)
    email = forms.EmailField(label='邮箱地址')
    password1 = format.CharField('密码', widget=forms.Passwordinput())
    password2 = format.CharField('确认密码', widget=forms.Passwordinput())

    def clean_username(self):

        #clean_*()方法将在指定字段的默认校验逻辑执行之后被调用。
        #如果一个Form实体的数据是合法的，它就会有一个可用的cleaned_data属性。
        #这是一个包含所有已经通过检验的数据的字典。
        
        username = self.clean_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('用户名中只能包含字母、数字和下划线')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('这个用户名已经被注册')

    def clean_email(self):
        email = self.clean_data['email']
        try:
            User.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError('邮箱地址已经被注册，请输入其他地址')

    def clean_password2(self):
        if 'password1' in self.clean_data:
            password1 = self.clean_data['password1']
            password2 = self.clean_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('两次输入的密码不一致')


class MsgPostForm(forms.Form):
    title = forms.CharField(label='标题',
                widget=forms.TextInput(attrs={'size': 30, 'max_length': 30}))
    content = forms.CharField(label='内容',
                widget=forms.Textarea(attrs={'size': 10000}))
'''


class MyComment(CommentForm):
    name = forms.CharField(label='您的名字', max_length=50)
    email = forms.EmailField(label='您的Email地址')
    url = forms.URLField(label='您的个人主页', required=False)
    comment = forms.CharField(label='您的评论', widget=forms.Textarea,
                                    max_length=10000)
    honeypot = forms.CharField(required=False,
                    label='这是防止恶意自动提交评论用的，请不要在此栏填写内容')

    def get_comment_create_data(self):
        data = super(MyComment, self).get_comment_create_data()
        return data
