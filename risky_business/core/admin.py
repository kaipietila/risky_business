from django.contrib import admin

from core.models import nlp
from core.models import aup


class SnippetResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'create_time', 'is_against_aup', 'snippet_text']
    search_fields = ['id']

    def snippet_text(self, obj):
        return obj.snippet.text


admin.site.register(nlp.Snippet)
admin.site.register(nlp.SnippetResults, SnippetResultsAdmin)
admin.site.register(aup.AcceptableUsePolicyRule)
admin.site.register(aup.Keyword)
admin.site.register(aup.Phrase)