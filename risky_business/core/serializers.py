from rest_framework import serializers

from core.models.nlp import Entity
from core.models.nlp import Snippet

class SnippetSerializer(serializers.Serializer):
    text = serializers.CharField()

class EntitySerializer(serializers.Serializer):
    id = serializers.UUIDField()
    risk_level = serializers.IntegerField()
    risk_text = SnippetSerializer()
