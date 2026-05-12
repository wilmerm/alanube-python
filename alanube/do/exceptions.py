from dataclasses import dataclass
from typing import Any, List, Optional
import requests


NON_FIELD_ERRORS = "non_field_errors"


@dataclass
class APIErrorItem:
    """
    This represents an individual error in the new unified API format.

    Attributes:
        `code`: Unique identifier for the error (e.g., "INVALID_FIELD").
        `message`: Diagnostic description of the error in English.
        `field`: Field associated with the error, when applicable. Can be None.
    """
    code: str
    message: str
    field: Optional[str] = None


def _parse_error_response(errors: Any) -> List[APIErrorItem]:
    """
    Parses the API error response and returns a list of APIErrorItems.

    Supports both the new unified format and legacy formats to maintain
    backward compatibility during the transition.

    New format:
        ```json
        { "code": 400, "errors": [ { "code": "...", "message": "...", "field": "..." } ] }
        ```

    Legacy formats:
        ```
        { "code": 400, "message": ["error message"] }
        { "code": 400, "errors": ["error message"] }
        { "errors": ["error message"] }
        ```

    """
    items: List[APIErrorItem] = []

    if isinstance(errors, dict):
        # --- New unified format ---
        raw_errors = errors.get("errors")
        if isinstance(raw_errors, list):
            for raw in raw_errors:
                if isinstance(raw, dict) and "code" in raw and "message" in raw:
                    items.append(APIErrorItem(
                        code=str(raw["code"]),
                        message=str(raw["message"]),
                        field=str(raw["field"]) if raw.get("field") else None,
                    ))
                elif isinstance(raw, str):
                    # Legacy: errors as a list of strings
                    items.append(APIErrorItem(
                        code="UNKNOWN",
                        message=raw,
                        field=None,
                    ))
            if items:
                return items

        # --- Legacy formats (dict with "message" or "errors" as a list/string) ---
        for key in ("message", "errors"):
            raw = errors.get(key)
            if isinstance(raw, list):
                for msg in raw:
                    if isinstance(msg, str):
                        items.append(APIErrorItem(code="UNKNOWN", message=msg, field=None))
                if items:
                    return items
            elif isinstance(raw, str):
                items.append(APIErrorItem(code="UNKNOWN", message=raw, field=None))
                return items

        # --- Fallback: take the entire dict as a string representation ---
        items.append(APIErrorItem(code="UNKNOWN", message=str(errors), field=None))

    elif isinstance(errors, list):
        # Legacy: errors as a flat list of strings
        for msg in errors:
            if isinstance(msg, str):
                items.append(APIErrorItem(code="UNKNOWN", message=msg, field=None))

    if not items:
        items.append(APIErrorItem(code="UNKNOWN", message=str(errors), field=None))

    return items


class AlanubeError(Exception):
    """Base class for all Alanube exceptions."""
    pass


class APIError(AlanubeError):
    """
    Exception raised for API errors.

    Attributes:
        message:      explanation of the error
        errors:       list of APIErrorItem parsed from the API response
        error_items:  alias for errors (list of APIErrorItem)
        response:     the HTTP response object
        status_code:  HTTP status code if available
        url:          request URL if available
    """

    def __init__(
        self,
        message: Optional[str] = None,
        errors: Optional[dict] = None,
        response: Optional[requests.Response] = None,
    ):
        self.response = response
        self.status_code = getattr(response, "status_code", None)
        self.url = getattr(response, "url", None)

        # Parse the errors to the new unified format
        self.error_items: List[APIErrorItem] = _parse_error_response(errors or {})
        self.errors: List[APIErrorItem] = self.error_items  # alias for compatibility

        if message:
            final_message = message
        elif self.error_items:
            # Use the first available message as the main message
            final_message = self.error_items[0].message
        elif self.status_code or self.url:
            final_message = f"{self.status_code or 'N/A'}: {self.url or 'unknown url'}"
        else:
            final_message = "API error without response"

        self.message = final_message
        super().__init__(final_message)

    @property
    def messages(self):
        """Return a list of error messages from parsed error items."""
        return [item.message for item in self.error_items]


class ObjectDoesNotExist(APIError):
    """Exception raised when an object does not exist."""
    pass


class NotFound(ObjectDoesNotExist):
    """Exception raised when a requested resource is not found."""
    pass


class ValidationError(APIError):
    """Exception raised for validation errors."""
    pass


class RequiredFieldMissingError(ValidationError):
    """Exception raised when a required field is missing."""
    pass


class ReadOnlyFieldError(ValidationError):
    """Exception raised when a read-only field is being modified."""
    pass


class InvalidFieldTypeError(ValidationError):
    """Exception raised when a field has an invalid type."""
    pass


class UnexpectedResponseCodeError(APIError):
    """
    Exception raised when the response code is unexpected.

    Attributes:
        expected_code -- the expected HTTP status code
        received_code -- the received HTTP status code
    """
    def __init__(self, expected_code: Optional[int], received_code: int, response: Optional[requests.Response] = None):
        self.expected_code = expected_code
        self.received_code = received_code
        message = f"Expected response code {expected_code}, but received {received_code}"
        super().__init__(message=message, response=response)


def handle_response_error(response: requests.Response, expected_response_code: Optional[int] = None):
    """
    Handle errors from the API response.

    Raises an appropriate error based on the response status code.
    """
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        try:
            errors = response.json()
        except ValueError:
            # If response is not a valid JSON, raise the original error
            raise e

        if response.status_code == 400:
            raise ValidationError(errors=errors, response=response)
        elif response.status_code == 404:
            raise NotFound(errors=errors, response=response)
        elif response.status_code == 500:
            raise APIError(errors=errors, response=response)

        raise APIError(errors=errors, response=response)

    # A successful response may still contain data indicating a failure.
    try:
        data = response.json()
    except ValueError:
        data = {'content': str(response.content)}

    if isinstance(data, dict) and data.get('httpStatusCode') in (400, 404, 500):
        # We throw a generic `APIError` since the error is
        # not directly related to the resource queried
        raise APIError(errors=data, response=response)

    if expected_response_code and expected_response_code != response.status_code:
        raise UnexpectedResponseCodeError(
            expected_code=expected_response_code,
            received_code=response.status_code,
            response=response,
        )
