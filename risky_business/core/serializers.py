from rest_framework import serializers
from core.models.nlp import Snippet


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('code', 'text', 'entity_id', 'risk_level', 'create_time',
                    'process_time',)
        read_only_fields = ('code', 'create_time', 'process_time',)
