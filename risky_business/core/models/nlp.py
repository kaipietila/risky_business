from django.db import models
import uuid

class Entity(models.Model):
    """
    The company or equivalent related to the analysed snippet
    """
    code = models.UUIDField(default=uuid.uuid4)
    risk_text = models.ForeignKey('Snippet', related_name='entity', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    risk_level = models.IntegerField(null=True)

class Snippet(models.Model):
    """
    The actual data to be analysed
    """
    code = models.UUIDField(default=uuid.uuid4)
    text = models.CharField(max_length=255)
    process_time = models.DateTimeField()
    results = models.OneToOneField('SnippetResults', on_delete=models.CASCADE)

class SnippetResults(models.Model):
    """
    Results are stored as pickled objects
    """
    results = models.BinaryField()


    