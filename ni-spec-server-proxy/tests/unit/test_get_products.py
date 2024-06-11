"""Contains test to validate the get_products API."""

from werkzeug.test import Client

from ni_spec_server_proxy.constants import ScmResponseStateCodes
from ni_spec_server_proxy.main import TAKE_COUNT
from tests.constants import DATA, STATE, STATUS_SUCCESS_RESPONSE_CODE


def test___connected_to_sle___get_products___returns_available_products(client: Client):
    response = client.get("/niscm/public/products")

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_response[DATA]) <= TAKE_COUNT
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS
