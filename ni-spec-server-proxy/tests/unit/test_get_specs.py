"""Contains tests to validate get_specs API."""

from werkzeug.test import Client

from ni_spec_server_proxy.constants import ScmResponseStateCodes
from tests.constants import (
    DATA,
    INVALID_PRODUCT_NAME,
    NO_SPEC_PRODUCT_NAME,
    STATE,
    STATUS_NOT_FOUND,
    STATUS_SUCCESS,
    VALID_PRODUCT_NAME,
    VALID_PRODUCT_REVISION,
)


def test___valid_product___get_specs___returns_specs(client: Client):
    """Test the get_specs with a valid product."""
    response = client.get(f"/niscm/public/spec/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}")

    assert response.status_code == STATUS_SUCCESS
    assert len(response.get_json()[DATA]) != 0
    assert response.get_json()[STATE] == ScmResponseStateCodes.SUCCESS


def test___valid_product___get_specs___returns_no_specs(client: Client):
    response = client.get(f"/niscm/public/spec/{NO_SPEC_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}")

    jsonified_response = response.get_json()
    assert response.status_code == STATUS_SUCCESS
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___invalid_product___get_specs___returns_product_not_found(client: Client):
    response = client.get(f"/niscm/public/spec/{INVALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}")

    jsonified_response = response.get_json()
    assert response.status_code == STATUS_NOT_FOUND
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE
