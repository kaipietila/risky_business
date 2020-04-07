from django.contrib import admin

from core.models.nlp import Snippet
from core.models.nlp import SnippetResults
from core.models.nlp import AcceptableUsePolicyRule

admin.site.register(Snippet)
admin.site.register(SnippetResults)
admin.site.register(AcceptableUsePolicyRule)
