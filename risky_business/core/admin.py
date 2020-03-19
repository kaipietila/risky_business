from django.contrib import admin

from core.models.nlp import Snippet, SnippetResults

admin.site.register(Snippet)

admin.site.register(SnippetResults)
