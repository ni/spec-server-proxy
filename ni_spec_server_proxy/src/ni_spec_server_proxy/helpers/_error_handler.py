"""Implementation of error handlers for flask server."""

from functools import wraps
from typing import Callable

from flask import Response, jsonify
from nisystemlink.clients.core import ApiException as NiSystemlinkException
from systemlink.clients.nifile.exceptions import ApiException as FileServicesException
from systemlink.clients.nitestmonitor.exceptions import ApiException as TestMonitorException

from ni_spec_server_proxy.constants import ResponseField, ScmResponseStateCodes, StatusCode


def get_error_response(error_message: str, status_code: int) -> Response:
    """Get error message response.

    Args:
        error_message (str): Error message to be displayed in the response.
        status_code (int): Status code of the error response.

    Returns:
        Response: Error response.
    """
    response = jsonify(
        {
            ResponseField.DATA: {},
            ResponseField.MESSAGE: error_message,
            ResponseField.STATE: ScmResponseStateCodes.FAILURE,
        }
    )
    response.status_code = status_code
    return response


def handle_errors(error_message: str) -> Callable:
    """Handle errors by providing a custom error message.

    It can be applied to Flask route functions to catch exceptions that occur\
    during their execution.

    Args:
        error_message (str): Custom error message to be included in the response.

    Returns:
        Callable: Decorated route function.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result

            except NiSystemlinkException as err:
                response = get_error_response(
                    error_message=str(err),
                    status_code=err.http_status_code,
                )
                return response

            except (TestMonitorException, FileServicesException) as err:
                response = get_error_response(error_message=str(err), status_code=err.status)
                return response

            except Exception:
                response = get_error_response(
                    error_message=error_message,
                    status_code=StatusCode.INTERNAL_SERVER_ERROR,
                )
                return response

        return wrapper

    return decorator
