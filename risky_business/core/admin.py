from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from core.forms import PhraseForm
from core.models import nlp
from core.models import aup


class SnippetResultsAdmin(admin.ModelAdmin):
    list_display = ['id', 'create_time', 'is_against_aup', 'snippet_text',
                    'snippet_url']
    search_fields = ['id']

    def snippet_text(self, obj):
        return obj.snippet.text

    def snippet_url(self, obj):
        url = reverse('admin:core_snippet_change', args=[obj.snippet.id])
        return format_html('<a href="{}">{}</a>', url, obj.snippet.id)


class SnippetAdmin(admin.ModelAdmin):
    list_display = ['code', 'create_time', 'text', 'process_time',
                    'entity_id', 'domicile', 'risk_level', 'results']
    search_fields = ['code', 'text', 'entity_id']

    def results(self, obj):
        for result in obj.results_set.all():
            url = reverse('admin:core_snippetresults_change', args=[result.id])
            return format_html('<a href="{}">{}</a>', url, result.id)


class PhraseAdmin(admin.ModelAdmin):
    list_display = ['phrase', 'risk_weight', 'language', 'pattern',
                    'aup']
    search_fields = ['phrase']
    list_filter = ['language']
    form = PhraseForm

    def aup(self, obj):
        aups = obj.aup_rule.all()
        urls = [(reverse('admin:core_acceptableusepolicyrule_change',
                         args=[aup.id]), aup.id) for aup in aups]
        html = ''
        for url, aup_id in urls:
            html += '<a href="{}">{}</a>, '.format(url, aup_id)
        return format_html(html)


admin.site.register(nlp.Snippet, SnippetAdmin)
admin.site.register(nlp.SnippetResults, SnippetResultsAdmin)
admin.site.register(aup.AcceptableUsePolicyRule)
admin.site.register(aup.Keyword)
admin.site.register(aup.Phrase, PhraseAdmin)
