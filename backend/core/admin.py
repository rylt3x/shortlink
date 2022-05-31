from django.contrib import admin
from core import models


@admin.register(models.SourceLink)
class SourceLinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_link', 'forward_link', 'created_at']
    readonly_fields = ('created_at', )
    ordering = ('-id', )


@admin.register(models.LinkFollow)
class LinkFollowAdmin(admin.ModelAdmin):
    list_display = ['link_pair', 'user_agent', 'ip_address', 'created_at']
    readonly_fields = ('created_at', )


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'description', 'headline_h1']
    list_editable = ['slug', 'description', 'headline_h1']
    prepopulated_fields = {'slug': ('title', )}
    readonly_fields = ('modified_at', )
    ordering = ('id', )
