
from typing import List, Tuple
from .api import Session
from . import dgii


class Alanube:

    def __init__(self, token: str, developer_mode=False):
        self.session = Session(token, developer_mode)


class AlanubeDGII(Alanube):

    def create_simple_cancellations(self, rnc_sender: int, sequences: List[Tuple[str, str]]):
        """
        Crea una cancelacción de NCF de manera simple.

        Args:
        ---------
        * `rnc_sender` (int): Corresponde al Número de Registro Nacional del
            contribuyente que emite la factura electrónica.
        * `sequences` (List[Tuple[str, str]]): Una lista de rangos
            (secuencia_inicial, secuencia_final) de los comprobantes que se van a anular.

        Returns:
        ---------
        (CancellationForm, Response): Retorna una tupla.

        Example:
        ---------
        >>> create_simple_cancellation(
            rnc_sender='132000000',
            sequences=[
                ('E310000000001', 'E310000000010'),
                ('E320000000004', 'E310000000005'),
            ]
        )
        (CancellationForm, Response)

        """
        form = dgii.create_simple_cancellations_form(rnc_sender, sequences)
        url = self.get_cancellations_url()
        response = self.session.post(url, json=form.data)
        return (form, dgii.Cancellation(response))

    def create_invoice(self, form: dgii.forms.InvoiceForm | dgii.forms.CreditNoteForm):
        """Create an invoice

        Returns:
            ```
            dgii.Invoice({
                "id": "01H22Z1JS88EWQCB4HZ9499TZ3",
                "stampDate": "1990-12-31",
                "status": "REGISTERED",
                "companyIdentification": 133109124,
                "encf": "E310000000005"
            })
            ```
        """
        encf = form.id_doc.encf
        url = self.get_url_from_encf(encf)
        response = self.session.post(url, json=form.data)
        return dgii.Invoice(response)

    def check_status(self, encf: str, status_id: str):
        """Consulta el estado de la factura electrónica"""
        url = self.get_url_from_encf(encf) + f'/{status_id}'
        res = self.session.get(url)
        return dgii.InvoiceStatus(res)

    def get_cancellations_url(self):
        return self.session.build_url('cancellations')

    def get_url_from_encf(self, encf: str):
        endpoint = self.get_endpoint_from_ncf(encf)
        return self.session.build_url(endpoint)

    def get_endpoint_from_ncf(self, encf: str):
        serie, code, sequence = dgii.utils.split_ncf(encf)

        encf_code_endpoint_map = {
            dgii.config.NCF_E_31: 'fiscal-invoices',
            dgii.config.NCF_E_32: 'invoices',
            dgii.config.NCF_E_33: 'debit-notes',
            dgii.config.NCF_E_34: 'credit-notes',
            dgii.config.NCF_E_41: 'purchases',
            dgii.config.NCF_E_43: 'minor-expenses',
            dgii.config.NCF_E_44: 'special-regimes',
            dgii.config.NCF_E_45: 'gubernamentals',
            # NCF_E_46: 'export-supports' FIXME: No hay información de esto en la DGII
            # NCF_E_47: 'payment-abroad-supports', FIXME: No hay información de esto en la DGII
        }
        return encf_code_endpoint_map[code]