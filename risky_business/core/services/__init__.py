from core.services.en_nlp import EnglishNLPService
from core.services.de_nlp import GermanNLPService
from core.services.fi_nlp import FinnishNLPService


def get_nlp_service(snippet):
    if snippet.domicile == 'GB':
        service = EnglishNLPService
    elif snippet.domicile == 'DE':
        service = GermanNLPService
    elif snippet.domicile == 'FI':
        service = FinnishNLPService
    return service
