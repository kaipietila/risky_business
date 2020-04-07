from django.core.management.base import BaseCommand
from django.db import transaction
import os
import json

from core.models.nlp import AcceptableUsePolicyRule

class Command(BaseCommand):
    help = 'Populate AUP to admin'

    @transaction.atomic
    def handle(self, *args, **options):
        filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                'tests/aup_fixture.json')
        with open(filepath) as aup_file:
            aup = json.load(aup_file)

        for index, rule in enumerate(aup):
            kwargs = {
                'id': index,
                'full_rule': rule['rule']
            }
            AcceptableUsePolicyRule.objects.create(**kwargs)

            print(f"Created AUP rule {index}")
