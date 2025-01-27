

import functools
import warnings


def build_url(url, company_id: str = None, id_: str = None, **params) -> str:
    """
    Build a URL from the given parameters.
    """
    if id_:
        url += f'/{id_}'

    if company_id:
        url += f'/idCompany/{company_id}'

    query_params = build_query_params(**params)
    if query_params:
        url += f"?{query_params}"

    return url


def build_query_params(**params) -> str:
    """
    Build a query string from the given parameters.
    """
    return "&".join([f"{camel_case(k)}={v}" for k, v in params.items() if v is not None])


def camel_case(name):
    """
    Convert snake_case to camelCase.
    """
    parts = name.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


def snake_case(name):
    """
    Convert camelCase to snake_case.
    """
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')


def deprecated(message=None):
    """
    This is a decorator which can be used to mark functions as deprecated.
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            warning_message = f"Call to deprecated function {func.__name__}."
            if message:
                warning_message += f" {message}"
            warnings.warn(warning_message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper

    # Permite usar el decorador tanto con paréntesis como sin ellos
    if callable(message):
        return decorator(message)

    return decorator
