from django.contrib import admin

from core.models.nlp import Entity, Snippet

admin.site.register(Entity)
admin.site.register(Snippet)
