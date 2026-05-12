import unittest
from unittest.mock import MagicMock, patch

import requests

from alanube.do import Alanube
from alanube.do.api import APIConfig, AlanubeAPI
from alanube.do.exceptions import (
    APIError,
    APIErrorItem,
    NotFound,
    ValidationError,
    _parse_error_response,
    handle_response_error,
)


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


class TestAPIErrorParsing(unittest.TestCase):
    """Tests para el parseo del nuevo formato unificado de errores de la API."""

    # --- _parse_error_response ---

    def test_new_unified_format(self):
        """El nuevo formato unificado se parsea correctamente."""
        error_data = {
            "code": 400,
            "errors": [
                {"code": "INVALID_FIELD", "message": "Invalid field value", "field": "name"},
                {"code": "REQUIRED", "message": "Field is required", "field": "email"},
            ]
        }
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].code, "INVALID_FIELD")
        self.assertEqual(items[0].message, "Invalid field value")
        self.assertEqual(items[0].field, "name")
        self.assertEqual(items[1].code, "REQUIRED")
        self.assertEqual(items[1].message, "Field is required")
        self.assertEqual(items[1].field, "email")

    def test_new_format_without_field(self):
        """El campo 'field' es opcional en el nuevo formato."""
        error_data = {
            "code": 500,
            "errors": [
                {"code": "INTERNAL_ERROR", "message": "Internal server error"},
            ]
        }
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].code, "INTERNAL_ERROR")
        self.assertEqual(items[0].message, "Internal server error")
        self.assertIsNone(items[0].field)

    def test_legacy_format_message_list(self):
        """Formato legacy: { 'code': 400, 'message': ['error msg'] }"""
        error_data = {"code": 400, "message": ["error message"]}
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].message, "error message")
        self.assertEqual(items[0].code, "UNKNOWN")

    def test_legacy_format_errors_list(self):
        """Formato legacy: { 'code': 400, 'errors': ['error msg'] }"""
        error_data = {"code": 400, "errors": ["error message"]}
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].message, "error message")
        self.assertEqual(items[0].code, "UNKNOWN")

    def test_legacy_format_errors_only(self):
        """Formato legacy: { 'errors': ['error message'] }"""
        error_data = {"errors": ["error message"]}
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].message, "error message")

    def test_legacy_format_plain_string(self):
        """Formato legacy: { 'message': 'single error string' }"""
        error_data = {"message": "single error"}
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].message, "single error")

    def test_new_format_takes_precedence_over_legacy(self):
        """Si están presentes ambos formatos, el nuevo formato tiene prioridad."""
        error_data = {
            "code": 400,
            "errors": [
                {"code": "VALIDATION", "message": "Validation failed", "field": "amount"},
            ],
            "message": ["legacy message"],
        }
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].code, "VALIDATION")
        self.assertEqual(items[0].message, "Validation failed")

    def test_empty_errors_list(self):
        """Lista de errores vacía produce un fallback con str(errors)."""
        error_data = {"code": 400, "errors": []}
        items = _parse_error_response(error_data)
        self.assertEqual(len(items), 1)

    def test_empty_dict(self):
        """Dict vacío produce un fallback."""
        items = _parse_error_response({})
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].code, "UNKNOWN")

    def test_plain_list(self):
        """Lista plana de strings (legacy)."""
        items = _parse_error_response(["error one", "error two"])
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].message, "error one")
        self.assertEqual(items[1].message, "error two")

    # --- APIError ---

    def test_api_error_message_from_error_items(self):
        """APIError usa el primer mensaje de error_items como message."""
        error_data = {
            "code": 400,
            "errors": [{"code": "BAD_REQUEST", "message": "Invalid input", "field": "amount"}]
        }
        exc = APIError(errors=error_data)
        self.assertEqual(exc.message, "Invalid input")
        self.assertEqual(len(exc.error_items), 1)
        self.assertEqual(exc.error_items[0].code, "BAD_REQUEST")

    def test_api_error_messages_property(self):
        """La property messages retorna todos los mensajes del array errors."""
        error_data = {
            "code": 400,
            "errors": [
                {"code": "E1", "message": "Error one"},
                {"code": "E2", "message": "Error two"},
            ]
        }
        exc = APIError(errors=error_data)
        self.assertEqual(exc.messages, ["Error one", "Error two"])

    def test_api_error_errors_alias(self):
        """errors y error_items son equivalentes y apuntan al mismo objeto."""
        error_data = {
            "code": 400,
            "errors": [{"code": "E1", "message": "Error"}]
        }
        exc = APIError(errors=error_data)
        self.assertIs(exc.errors, exc.error_items)

    def test_api_error_message_explicit_overrides(self):
        """Si se pasa un message explícito, se usa en lugar del de error_items."""
        exc = APIError(message="Custom error message")
        self.assertEqual(exc.message, "Custom error message")
        self.assertIsInstance(exc.error_items, list)

    def test_api_error_errors_none_no_response(self):
        """Si errors es None y no hay response, no falla."""
        exc = APIError()
        self.assertIsInstance(exc.error_items, list)
        self.assertIsNone(exc.status_code)
        self.assertIsNone(exc.url)

    def test_api_error_status_code_and_url_from_response(self):
        """status_code y url se toman del response."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = 403
        mock_response.url = "https://api.test/resource"

        exc = APIError(response=mock_response)
        self.assertEqual(exc.status_code, 403)
        self.assertEqual(exc.url, "https://api.test/resource")

    # --- Subclases ---

    def test_validation_error_inherits_parsing(self):
        """ValidationError hereda correctamente el parseo del nuevo formato."""
        error_data = {
            "code": 400,
            "errors": [{"code": "REQUIRED", "message": "Field is required", "field": "name"}]
        }
        exc = ValidationError(errors=error_data)
        self.assertEqual(exc.message, "Field is required")
        self.assertEqual(exc.error_items[0].code, "REQUIRED")

    def test_not_found_inherits_parsing(self):
        """NotFound hereda correctamente el parseo del nuevo formato."""
        error_data = {
            "code": 404,
            "errors": [{"code": "NOT_FOUND", "message": "Resource not found"}]
        }
        exc = NotFound(errors=error_data)
        self.assertEqual(exc.message, "Resource not found")
        self.assertEqual(exc.error_items[0].code, "NOT_FOUND")

    # --- handle_response_error ---

    def _make_error_response(self, status_code, json_data, url="https://sandbox.alanube.co/dom/v1/test"):
        """Crea un mock de requests.Response que lance HTTPError en raise_for_status."""
        mock_response = MagicMock(spec=requests.Response)
        mock_response.status_code = status_code
        mock_response.json.return_value = json_data
        mock_response.url = url
        # Simular raise_for_status: lanza HTTPError si status_code es de error
        if status_code >= 400:
            mock_response.raise_for_status.side_effect = requests.HTTPError(response=mock_response)
        return mock_response

    def test_handle_response_error_400_new_format(self):
        """handle_response_error lanza ValidationError con el nuevo formato."""
        mock_response = self._make_error_response(400, {
            "code": 400,
            "errors": [{"code": "REQUIRED", "message": "Field is required", "field": "name"}]
        })

        with self.assertRaises(ValidationError) as ctx:
            handle_response_error(mock_response)
        self.assertEqual(ctx.exception.message, "Field is required")
        self.assertEqual(ctx.exception.error_items[0].code, "REQUIRED")
        self.assertEqual(ctx.exception.error_items[0].field, "name")

    def test_handle_response_error_404_new_format(self):
        """handle_response_error lanza NotFound con el nuevo formato."""
        mock_response = self._make_error_response(404, {
            "code": 404,
            "errors": [{"code": "NOT_FOUND", "message": "The requested resource was not found"}]
        })

        with self.assertRaises(NotFound) as ctx:
            handle_response_error(mock_response)
        self.assertEqual(ctx.exception.message, "The requested resource was not found")
        self.assertEqual(ctx.exception.error_items[0].code, "NOT_FOUND")

    def test_handle_response_error_500_new_format(self):
        """handle_response_error lanza APIError con el nuevo formato en 500."""
        mock_response = self._make_error_response(500, {
            "code": 500,
            "errors": [{"code": "INTERNAL_ERROR", "message": "Internal server error occurred"}]
        })

        with self.assertRaises(APIError) as ctx:
            handle_response_error(mock_response)
        self.assertEqual(ctx.exception.message, "Internal server error occurred")

    def test_handle_response_error_400_legacy_format(self):
        """handle_response_error funciona con formato legacy (retrocompatibilidad)."""
        mock_response = self._make_error_response(400, {
            "code": 400,
            "errors": ["legacy error message"]
        })

        with self.assertRaises(ValidationError) as ctx:
            handle_response_error(mock_response)
        self.assertEqual(ctx.exception.message, "legacy error message")
        self.assertEqual(ctx.exception.error_items[0].code, "UNKNOWN")

    def test_handle_response_error_http_status_code_in_success(self):
        """Respuesta 200 con httpStatusCode de error lanza APIError."""
        mock_response = self._make_error_response(200, {
            "httpStatusCode": 400,
            "errors": [{"code": "VALIDATION", "message": "Validation error in success response"}]
        })

        with self.assertRaises(APIError) as ctx:
            handle_response_error(mock_response)
        self.assertEqual(ctx.exception.message, "Validation error in success response")
        self.assertEqual(ctx.exception.error_items[0].code, "VALIDATION")

    # --- APIErrorItem ---

    def test_api_error_item_dataclass(self):
        """APIErrorItem es un dataclass con los campos correctos."""
        item = APIErrorItem(code="TEST", message="Test message", field="testField")
        self.assertEqual(item.code, "TEST")
        self.assertEqual(item.message, "Test message")
        self.assertEqual(item.field, "testField")

    def test_api_error_item_default_field_none(self):
        """field por defecto es None."""
        item = APIErrorItem(code="TEST", message="Test message")
        self.assertIsNone(item.field)
