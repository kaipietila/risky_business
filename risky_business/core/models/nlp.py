from django.db import models

class Entity(models.Model):
    """
    The company or equivalent related to the analysed snippet
    """
    risk_text = models.ForeignKey('Snippet', related_name='entity', on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    risk_level = models.IntegerField()

class Snippet(models.Model):
    """
    The actual data to be analysed
    """
    text = models.CharField()
    process_time = models.DateTimeField()
    results = models.OneToOneField('SnippetResults', on_delete=models.CASCADE)

class SnippetResults(models.Model):
    """
    Results are stored as pickled objects
    """
    results = models.BinaryField()


    