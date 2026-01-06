from typing import Optional
import requests


NON_FIELD_ERRORS = "non_field_errors"


class AlanubeError(Exception):
    """Base class for all Alanube exceptions."""
    pass


class APIError(AlanubeError):
    """
    Exception raised for API errors.

    Attributes:
        message:      explanation of the error
        errors:       errors returned by the API
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
        self.errors = errors or {}
        self.status_code = getattr(response, "status_code", None)
        self.url = getattr(response, "url", None)

        if message:
            final_message = message
        elif self.errors:
            final_message = self.errors.get("message") or str(self.errors)
        elif self.status_code or self.url:
            final_message = f"{self.status_code or 'N/A'}: {self.url or 'unknown url'}"
        else:
            final_message = "API error without response"

        self.message = final_message
        super().__init__(final_message)

    @property
    def messages(self):
        """Return a list of error messages."""
        return [e2 for e1 in self.errors.values() for e2 in (e1 if isinstance(e1, list) else [e1])]


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
