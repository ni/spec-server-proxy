"""Contains tests to validate get_specs API."""

from werkzeug.test import Client

from ni_spec_server_proxy.constants import ScmResponseStateCodes
from tests.constants import (
    DATA,
    INVALID_PRODUCT_GET_SPEC_URL,
    NO_SPEC_PRODUCT_GET_SPEC_URL,
    STATE,
    STATUS_NOT_FOUND_RESPONSE_CODE,
    STATUS_SUCCESS_RESPONSE_CODE,
    VALID_PRODUCT_GET_SPEC_URL,
)


def test___valid_product___get_specs___returns_specs(client: Client):
    response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_response[DATA]) != 0
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___no_spec_product___get_specs___returns_no_specs(client: Client):
    response = client.get(NO_SPEC_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___invalid_product___get_specs___returns_product_not_found(client: Client):
    response = client.get(INVALID_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_NOT_FOUND_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE
