from django.contrib import admin

from core.models import nlp
from core.models import aup

admin.site.register(nlp.Snippet)
admin.site.register(nlp.SnippetResults)
admin.site.register(aup.AcceptableUsePolicyRule)
admin.site.register(aup.Keyword)
admin.site.register(aup.Phrase)