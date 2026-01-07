import unittest
from unittest.mock import MagicMock, patch

from alanube.do import Alanube
from alanube.do.api import APIConfig, AlanubeAPI
from alanube.do.exceptions import ValidationError


class TestAlanube(unittest.TestCase):
    @patch("alanube.do.Alanube.get_document_func_map")
    def test_get_document(self, mock_get_document_func_map):
        mock_get_document_func_map.get.return_value = None
        with self.assertRaises(NotImplementedError):
            Alanube.get_document(1, "123")

    @patch("alanube.do.Alanube.get_documents_func_map")
    def test_get_documents(self, mock_get_documents_func_map):
        mock_get_documents_func_map.get.return_value = None
        with self.assertRaises(NotImplementedError):
            Alanube.get_documents(1)

    def test_send_document_func_map(self):
        self.assertIsInstance(Alanube.send_document_func_map, dict)

    def test_get_document_func_map(self):
        self.assertIsInstance(Alanube.get_document_func_map, dict)

    def test_get_documents_func_map(self):
        self.assertIsInstance(Alanube.get_documents_func_map, dict)

    def test_get_document_func_map_values(self):
        for value in Alanube.get_document_func_map.values():
            self.assertTrue(callable(value))

    def test_get_documents_func_map_values(self):
        for value in Alanube.get_documents_func_map.values():
            self.assertTrue(callable(value))

    def test_get_document_func_map_keys(self):
        for key in Alanube.get_document_func_map.keys():
            self.assertIsInstance(key, int)

    def test_get_documents_func_map_keys(self):
        for key in Alanube.get_documents_func_map.keys():
            self.assertIsInstance(key, int)


class TestAlanubeAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.token = "test_token"
        cls.developer_mode = True
        cls.api_version = "v1"
        AlanubeAPI.connect(cls.token, cls.developer_mode, cls.api_version)

    def test_connect(self):
        self.assertIsInstance(AlanubeAPI.config, APIConfig)
        self.assertEqual(AlanubeAPI.config.token, self.token)
        self.assertEqual(AlanubeAPI.config.developer_mode, self.developer_mode)
        self.assertEqual(AlanubeAPI.config.api_version, self.api_version)

    @patch('alanube.do.api.requests.request')
    def test_get_company(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "name": "Test Company"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        company_id = "123"
        response = AlanubeAPI.get_company(company_id)
        self.assertEqual(response, {"id": "123", "name": "Test Company"})
        mock_request.assert_called_once_with(
            'GET',
            f'https://sandbox.alanube.co/dom/v1/company/{company_id}',
            headers=AlanubeAPI.get_headers(),
            params=None,
            json=None
        )

    @patch('alanube.do.api.requests.request')
    def test_create_company(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "name": "Test Company"}
        mock_response.status_code = 201
        mock_request.return_value = mock_response

        payload = {"name": "Test Company"}
        response = AlanubeAPI.create_company(payload)
        self.assertEqual(response, {"id": "123", "name": "Test Company"})
        mock_request.assert_called_once_with(
            'POST',
            'https://sandbox.alanube.co/dom/v1/company',
            headers=AlanubeAPI.get_headers(),
            params=None,
            json=payload
        )

    @patch('alanube.do.api.requests.request')
    def test_update_company(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "name": "Updated Company"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        payload = {"name": "Updated Company"}
        company_id = "123"
        response = AlanubeAPI.update_company(payload, company_id)
        self.assertEqual(response, {"id": "123", "name": "Updated Company"})
        mock_request.assert_called_once_with(
            'PATCH',
            f'https://sandbox.alanube.co/dom/v1/company/{company_id}',
            headers=AlanubeAPI.get_headers(),
            params=None,
            json=payload
        )

    @patch('alanube.do.api.requests.request')
    def test_send_fiscal_invoice(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "status": "sent"}
        mock_response.status_code = 201
        mock_request.return_value = mock_response

        payload = {"amount": 1000}
        response = AlanubeAPI.send_fiscal_invoice(payload)
        self.assertEqual(response, {"id": "123", "status": "sent"})
        mock_request.assert_called_once_with(
            'POST',
            'https://sandbox.alanube.co/dom/v1/fiscal-invoices',
            headers=AlanubeAPI.get_headers(),
            params=None,
            json=payload
        )

    @patch('alanube.do.api.requests.request')
    def test_get_fiscal_invoice(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "123", "status": "approved"}
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        invoice_id = "123"
        response = AlanubeAPI.get_fiscal_invoice(invoice_id)
        self.assertEqual(response, {"id": "123", "status": "approved"})
        mock_request.assert_called_once_with(
            'GET',
            f'https://sandbox.alanube.co/dom/v1/fiscal-invoices/{invoice_id}',
            headers=AlanubeAPI.get_headers(),
            params=None,
            json=None
        )

    def test_get_invoices_invalid_status_validation(self):
        with patch('alanube.do.api.requests.request') as mock_request:
            with self.assertRaises(ValidationError):
                AlanubeAPI.get_invoices(status="INVALID")
            mock_request.assert_not_called()

    def test_get_invoices_invalid_legal_status_validation(self):
        with patch('alanube.do.api.requests.request') as mock_request:
            with self.assertRaises(ValidationError):
                AlanubeAPI.get_invoices(legal_status="ACCEPTED,WRONG")
            mock_request.assert_not_called()

    def test_check_directory_invalid_rnc(self):
        with patch('alanube.do.api.requests.request') as mock_request:
            with self.assertRaises(ValidationError):
                AlanubeAPI.check_directory(rnc="123-456")
            mock_request.assert_not_called()

    def test_check_dgii_status_invalid_environment(self):
        with patch('alanube.do.api.requests.request') as mock_request:
            with self.assertRaises(ValidationError):
                AlanubeAPI.check_dgii_status(environment=4)
            mock_request.assert_not_called()

    def test_get_received_documents_invalid_pagination(self):
        with patch('alanube.do.api.requests.request') as mock_request:
            with self.assertRaises(ValidationError):
                AlanubeAPI.get_received_documents(limit=0)
            mock_request.assert_not_called()
