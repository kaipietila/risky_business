from django.db import models
import uuid


class Snippet(models.Model):
    """
    The actual data to be analysed
    """
    code = models.UUIDField(default=uuid.uuid4)
    text = models.CharField(max_length=255)
    process_time = models.DateTimeField(null=True, blank=True)
    processed = models.BooleanField(default=False)
    entity_id = models.CharField(max_length=255, blank=True)
    risk_level = models.IntegerField(null=True)
    create_time = models.DateTimeField(auto_now_add=True)


class SnippetResults(models.Model):
    """
    Results are stored as pickled objects
    """
    snippet = models.ForeignKey('Snippet', on_delete=models.PROTECT,
                                related_name='results', null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    results = models.BinaryField(null=True)
    