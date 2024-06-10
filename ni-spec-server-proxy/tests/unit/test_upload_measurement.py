"""Contains tests to validate upload_measurement API."""

import io

from werkzeug.datastructures import FileStorage
from werkzeug.test import Client

from ni_spec_server_proxy.constants import ScmResponseStateCodes
from tests.constants import (
    DATA,
    DISCIPLINE,
    INVALID_MEASUREMENT_FILE_NAME,
    INVALID_MEASUREMENT_FILE_PATH,
    INVALID_PRODUCT_NAME,
    STATE,
    STATUS_INTERNAL_SERVER_RESPONSE_CODE,
    STATUS_NOT_FOUND_RESPONSE_CODE,
    STATUS_SUCCESS_RESPONSE_CODE,
    SUCCESS_STATE_IN_FILE_UPLOAD,
    VALID_MEASUREMENT_FILE_NAME,
    VALID_MEASUREMENT_FILE_PATH,
    VALID_PRODUCT_NAME,
    VALID_PRODUCT_REVISION,
)


def test___valid_measurement_file___upload_measurement___returns_success_response(client: Client):
    with open(
        VALID_MEASUREMENT_FILE_PATH,
        "rb",
    ) as f:
        file_content = f.read()
    files = {
        "formCollection": (
            FileStorage(
                stream=io.BytesIO(file_content),
                filename=VALID_MEASUREMENT_FILE_NAME,
                content_type="text/csv",
            )
        )
    }

    response = client.post(
        f"/niscm/public/data/upload/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}",
        data=files,
        content_type="multipart/form-data",
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert jsonified_response[DATA]["fileName"] == VALID_MEASUREMENT_FILE_NAME
    assert not jsonified_response[DATA]["errors"]
    assert jsonified_response[STATE] == SUCCESS_STATE_IN_FILE_UPLOAD


def test___invalid_measurement_file___upload_measurement___returns_internal_server_error(
    client: Client,
):
    with open(
        INVALID_MEASUREMENT_FILE_PATH,
        "rb",
    ) as f:
        file_content = f.read()
    files = {
        "formCollection": (
            FileStorage(
                stream=io.BytesIO(file_content),
                filename=INVALID_MEASUREMENT_FILE_NAME,
                content_type="text/csv",
            )
        )
    }

    response = client.post(
        f"/niscm/public/data/upload/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}",
        data=files,
        content_type="multipart/form-data",
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_INTERNAL_SERVER_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE


def test___invalid_product___upload_measurement___returns_product_not_found(client: Client):
    with open(
        VALID_MEASUREMENT_FILE_PATH,
        "rb",
    ) as f:
        file_content = f.read()
    files = {
        "formCollection": (
            FileStorage(
                stream=io.BytesIO(file_content),
                filename=VALID_MEASUREMENT_FILE_NAME,
                content_type="text/csv",
            )
        )
    }

    response = client.post(
        f"/niscm/public/data/upload/{INVALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}",
        data=files,
        content_type="multipart/form-data",
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_NOT_FOUND_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE
