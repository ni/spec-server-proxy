"""Contains tests to validate Products and Specs APIs."""

from werkzeug import Client

from ni_spec_server_proxy.constants import ScmResponseStateCodes
from ni_spec_server_proxy.main import TAKE_COUNT
from tests.constants import (
    DATA,
    GET_PRODUCTS_URL,
    NO_SPEC_PRODUCT_GET_SPEC_URL,
    STATE,
    STATUS_SUCCESS_RESPONSE_CODE,
    VALID_PRODUCT_GET_SPEC_URL,
)


def test___connected_to_sle___available_products_available_specs___returns_success_response(
    client: Client,
) -> None:
    response = client.get(GET_PRODUCTS_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_response[DATA]) <= TAKE_COUNT
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS

    response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_response[DATA]) != 0
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___connected_to_sle___available_products_unavailable_specs___returns_success_response(
    client: Client,
) -> None:
    response = client.get(GET_PRODUCTS_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_response[DATA]) <= TAKE_COUNT
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS

    response = client.get(NO_SPEC_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS
