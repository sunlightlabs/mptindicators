from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Page, Chunk


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('slug',)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'is_published')

    fieldsets = (
        (None, {
            'fields': ('path', 'navbar', 'is_published'),
        }),
        ('Content', {
            'fields': ('title', 'intro', 'content', 'content_markup_type', 'sidebar'),
        }),
        ('Scripts and styles', {
            'classes': ('collapse',),
            'fields': ('css', 'js'),
        })
    )

    def get_queryset(self, request):
        return self.model.objects.filter(is_simplepage=True)


admin.site.register(Chunk, ChunkAdmin)
admin.site.register(Page, PageAdmin)
