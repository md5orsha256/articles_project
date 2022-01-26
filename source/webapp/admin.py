from django.contrib import admin

from webapp.models import Article, Comment, Type, Status


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at', "type", "status"]
    readonly_fields = ['created_at', 'updated_at']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Type)
admin.site.register(Status)
