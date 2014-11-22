#coding=utf-8
from django.contrib import admin
from models import BlogPost, Tag, Photo, Code, Paragraph, MyComment


class TagAdmin(admin.ModelAdmin):
    list_display = ('tag_name', )


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', )
    search_fields = ('title', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'author_email', 'created_at', 'blog')


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Photo)
admin.site.register(Code)
admin.site.register(Paragraph)
admin.site.register(MyComment, CommentAdmin)
