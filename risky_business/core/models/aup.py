from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.constants import AUPDecisionChoices


def _get_choices(choices):
    return (
        (choice.value, choice.name)
        for choice in choices
    )


class AcceptableUsePolicyRule(models.Model):
    """
    AUP rules modelled to the DB for easy config etc.
    """
    id = models.IntegerField(primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True)
    full_rule = models.CharField(max_length=512)
    hit_message = models.CharField(max_length=255, blank=True)
    decision = models.CharField(max_length=128,
                                choices=_get_choices(AUPDecisionChoices),
                                null=True)

    def __str__(self):
        return f'{self.full_rule}'


class Keyword(models.Model):
    """
    One word that we try to match
    e.g. cryptocurrency
    """
    keyword = models.CharField(max_length=255)
    aup_rule = models.ManyToManyField(AcceptableUsePolicyRule,
                                 related_name='keywords')
    risk_weight = models.IntegerField(null=True)
    language = models.CharField(max_length=2)

    def __str__(self):
        return self.keyword


class Phrase(models.Model):
    """
    Phrases can include multiple (e.g. 2-3) words in sequence
    e.g. real estate
    """
    phrase = models.CharField(max_length=255)
    aup_rule = models.ManyToManyField(AcceptableUsePolicyRule,
                                 related_name='phrases')
    risk_weight = models.IntegerField(null=True)
    language = models.CharField(max_length=2)

    def __str__(self):
        return self.phrase
