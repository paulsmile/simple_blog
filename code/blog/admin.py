#coding=utf-8
from django.contrib import admin
from models import BlogPost, Tag, Photo, Code


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', )


class BlogPostAdmin (admin.ModelAdmin):
    list_display = ('title', 'timestamp', )
    search_fields = ('title', )

admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Photo)
admin.site.register(Code)
