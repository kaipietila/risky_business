import json
from django import forms
from django.contrib.postgres.forms import JSONField

from core.models.aup import Phrase
from core.constants import SpacyPatternKeys


class PhraseForm(forms.ModelForm):
    pattern = JSONField(required=False)

    class Meta:
        model = Phrase
        fields = '__all__'

    def clean_pattern(self):
        pattern = self.cleaned_data['pattern']
        spacy_token_list = [key.value for key in SpacyPatternKeys]
        invalid_tokens = [next(iter(word)) for word in pattern if
                          next(iter(word)) not in spacy_token_list]
        if invalid_tokens:
            error_message = (f'Invalid word token(s) {invalid_tokens} in pattern, '
                             f'please consult spacy documentation for rule matcher')
            raise forms.ValidationError(error_message)
        return pattern