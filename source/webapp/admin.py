from django.contrib import admin

from webapp.models import Article, Comment, Tag


class MembershipInline(admin.TabularInline):
    model = Article.tags.through


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'created_at']
    list_filter = ['author']
    search_fields = ['title', 'content']
    fields = ['title', 'author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [
        MembershipInline,
    ]
    exclude = ('tags',)


class TagAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)
