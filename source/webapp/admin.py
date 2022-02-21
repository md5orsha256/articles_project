from django.contrib import admin

from webapp.models import Article, Comment, Tag


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'tags', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    fields = ['name', "created_at", "updated_at"]
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
