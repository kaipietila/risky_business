from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid

from core.services import get_nlp_service


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
    domicile = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.code}'

    @property
    def nlp_service(self):
        service = get_nlp_service(self)
        return service(self)


class SnippetResults(models.Model):
    """
    Results are stored as pickled objects
    """
    snippet = models.ForeignKey('Snippet', on_delete=models.PROTECT,
                                related_name='results_set', null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    binary_results = models.BinaryField(null=True)
    is_against_aup = models.BooleanField()
    assessed_risk_level = models.IntegerField(null=True)
    report = JSONField()

    def __str__(self):
        return f'results for {self.snippet}'
