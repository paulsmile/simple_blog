#! /usr/bin/env python
#coding=utf-8
from django import forms
from blog.models import MyComment


class MyCommentForm(forms.ModelForm):

    class Meta:
        model = MyComment
        fields = ('author', 'author_email', 'content')
