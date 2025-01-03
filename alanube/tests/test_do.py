import unittest
from unittest.mock import patch

from alanube.do.utils import (
    create_company,
    update_company,
    get_company,
    send_fiscal_invoice,
    get_fiscal_invoice_status,
    send_invoice,
    get_invoice_status,
    send_debit_note,
    get_debit_note_status,
    send_credit_note,
    get_credit_note_status,
    send_purchase,
    get_purchase_status,
    send_minor_expense,
    get_minor_expense_status,
    send_special_regime,
    get_special_regime_status,
    send_gubernamental,
    get_gubernamental_status,
    send_export_support,
    get_export_support_status,
    send_payment_abroad_support,
    get_payment_abroad_support_status,
    send_cancellation,
    get_cancellation_status,
    get_received_document,
    get_received_documents,
    check_directory
)


class TestUtils(unittest.TestCase):

    @patch('alanube.do.utils.AlanubeAPI.create_company')
    def test_create_company(self, mock_create_company):
        payload = {'name': 'Test Company'}
        create_company(payload)
        mock_create_company.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.update_company')
    def test_update_company(self, mock_update_company):
        payload = {'name': 'Updated Company'}
        company_id = '123'
        update_company(payload, company_id)
        mock_update_company.assert_called_once_with(payload, company_id)

    @patch('alanube.do.utils.AlanubeAPI.get_company')
    def test_get_company(self, mock_get_company):
        company_id = '123'
        get_company(company_id)
        mock_get_company.assert_called_once_with(company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_fiscal_invoice')
    def test_send_fiscal_invoice(self, mock_send_fiscal_invoice):
        payload = {'invoice': 'data'}
        send_fiscal_invoice(payload)
        mock_send_fiscal_invoice.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_fiscal_invoice_status')
    def test_get_fiscal_invoice_status(self, mock_get_fiscal_invoice_status):
        document_id = '123'
        company_id = '456'
        get_fiscal_invoice_status(document_id, company_id)
        mock_get_fiscal_invoice_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_invoice')
    def test_send_invoice(self, mock_send_invoice):
        payload = {'invoice': 'data'}
        send_invoice(payload)
        mock_send_invoice.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_invoice_status')
    def test_get_invoice_status(self, mock_get_invoice_status):
        document_id = '123'
        company_id = '456'
        get_invoice_status(document_id, company_id)
        mock_get_invoice_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_debit_note')
    def test_send_debit_note(self, mock_send_debit_note):
        payload = {'note': 'data'}
        send_debit_note(payload)
        mock_send_debit_note.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_debit_note_status')
    def test_get_debit_note_status(self, mock_get_debit_note_status):
        document_id = '123'
        company_id = '456'
        get_debit_note_status(document_id, company_id)
        mock_get_debit_note_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_credit_note')
    def test_send_credit_note(self, mock_send_credit_note):
        payload = {'note': 'data'}
        send_credit_note(payload)
        mock_send_credit_note.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_credit_note_status')
    def test_get_credit_note_status(self, mock_get_credit_note_status):
        document_id = '123'
        company_id = '456'
        get_credit_note_status(document_id, company_id)
        mock_get_credit_note_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_purchase')
    def test_send_purchase(self, mock_send_purchase):
        payload = {'purchase': 'data'}
        send_purchase(payload)
        mock_send_purchase.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_purchase_status')
    def test_get_purchase_status(self, mock_get_purchase_status):
        document_id = '123'
        company_id = '456'
        get_purchase_status(document_id, company_id)
        mock_get_purchase_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_minor_expense')
    def test_send_minor_expense(self, mock_send_minor_expense):
        payload = {'expense': 'data'}
        send_minor_expense(payload)
        mock_send_minor_expense.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_minor_expense_status')
    def test_get_minor_expense_status(self, mock_get_minor_expense_status):
        document_id = '123'
        company_id = '456'
        get_minor_expense_status(document_id, company_id)
        mock_get_minor_expense_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_special_regime')
    def test_send_special_regime(self, mock_send_special_regime):
        payload = {'regime': 'data'}
        send_special_regime(payload)
        mock_send_special_regime.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_special_regime_status')
    def test_get_special_regime_status(self, mock_get_special_regime_status):
        document_id = '123'
        company_id = '456'
        get_special_regime_status(document_id, company_id)
        mock_get_special_regime_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_gubernamental')
    def test_send_gubernamental(self, mock_send_gubernamental):
        payload = {'gubernamental': 'data'}
        send_gubernamental(payload)
        mock_send_gubernamental.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_gubernamental_status')
    def test_get_gubernamental_status(self, mock_get_gubernamental_status):
        document_id = '123'
        company_id = '456'
        get_gubernamental_status(document_id, company_id)
        mock_get_gubernamental_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_export_support')
    def test_send_export_support(self, mock_send_export_support):
        payload = {'export': 'data'}
        send_export_support(payload)
        mock_send_export_support.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_export_support_status')
    def test_get_export_support_status(self, mock_get_export_support_status):
        document_id = '123'
        company_id = '456'
        get_export_support_status(document_id, company_id)
        mock_get_export_support_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_payment_abroad_support')
    def test_send_payment_abroad_support(self, mock_send_payment_abroad_support):
        payload = {'payment': 'data'}
        send_payment_abroad_support(payload)
        mock_send_payment_abroad_support.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_payment_abroad_support_status')
    def test_get_payment_abroad_support_status(self, mock_get_payment_abroad_support_status):
        document_id = '123'
        company_id = '456'
        get_payment_abroad_support_status(document_id, company_id)
        mock_get_payment_abroad_support_status.assert_called_once_with(document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.send_cancellation')
    def test_send_cancellation(self, mock_send_cancellation):
        payload = {'cancellation': 'data'}
        send_cancellation(payload)
        mock_send_cancellation.assert_called_once_with(payload)

    @patch('alanube.do.utils.AlanubeAPI.get_cancellation_status')
    def test_get_cancellation_status(self, mock_get_cancellation_status):
        cancellation_id = '123'
        company_id = '456'
        get_cancellation_status(cancellation_id, company_id)
        mock_get_cancellation_status.assert_called_once_with(cancellation_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.get_received_document')
    def test_get_received_document(self, mock_get_received_document):
        received_document_id = '123'
        company_id = '456'
        get_received_document(received_document_id, company_id)
        mock_get_received_document.assert_called_once_with(received_document_id, company_id)

    @patch('alanube.do.utils.AlanubeAPI.get_received_documents')
    def test_get_received_documents(self, mock_get_received_documents):
        company_id = '456'
        limit = 25
        page = 1
        start = '2023-01-01'
        end = '2023-12-31'
        get_received_documents(company_id, limit, page, start, end)
        mock_get_received_documents.assert_called_once_with(company_id, limit, page, start, end)

    @patch('alanube.do.utils.AlanubeAPI.check_directory')
    def test_check_directory(self, mock_check_directory):
        rnc = '123456789'
        company_id = '456'
        check_directory(rnc, company_id)
        mock_check_directory.assert_called_once_with(rnc, company_id)


if __name__ == '__main__':
    unittest.main()