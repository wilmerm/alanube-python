from . import dgii


class Alanube:

    def __init__(self, token: str, api_url: str):
        self.__token = token
        self.__api_url = api_url


class AlanubeDGII(Alanube):

    def __init__(self, token: str, api_url: str = dgii.config.API_URL):
        super().__init__(token, api_url)

    def create_invoice(self, form: dgii.forms.InvoiceForm | dgii.forms.CreditNoteForm):
        response = dgii.Invoice.create(form)
        return response