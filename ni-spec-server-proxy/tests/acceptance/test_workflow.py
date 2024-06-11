"""Contains test case to validate valid workflow."""

import io

from werkzeug import Client
from werkzeug.datastructures import FileStorage

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from ni_spec_server_proxy.main import TAKE_COUNT
from tests.constants import (
    DATA,
    DISCIPLINE,
    INVALID_MEASUREMENT_FILE_NAME,
    INVALID_MEASUREMENT_FILE_PATH,
    INVALID_PRODUCT_GET_SPEC_URL,
    INVALID_PRODUCT_NAME,
    MESSAGE,
    STATE,
    STATUS_INTERNAL_SERVER_RESPONSE_CODE,
    STATUS_NOT_FOUND_RESPONSE_CODE,
    STATUS_SUCCESS_RESPONSE_CODE,
    SUCCESS_STATE_IN_FILE_UPLOAD,
    VALID_MEASUREMENT_FILE_NAME,
    VALID_MEASUREMENT_FILE_PATH,
    VALID_PRODUCT_GET_SPEC_URL,
    VALID_PRODUCT_NAME,
    VALID_PRODUCT_REVISION,
)


def test___connected_to_sle___product_available____returns_success_response(client: Client):
    products_response = client.get("/niscm/public/products")

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    specs_response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_specs_response = specs_response.get_json()

    assert specs_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_specs_response[DATA]) != 0
    assert jsonified_specs_response[STATE] == ScmResponseStateCodes.SUCCESS

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

    file_upload_response = client.post(
        f"/niscm/public/data/upload/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}",
        data=files,
        content_type="multipart/form-data",
    )

    jsonified_file_upload_response = file_upload_response.get_json()

    assert file_upload_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert jsonified_file_upload_response[DATA]["fileName"] == VALID_MEASUREMENT_FILE_NAME
    assert not jsonified_file_upload_response[DATA]["errors"]
    assert jsonified_file_upload_response[STATE] == SUCCESS_STATE_IN_FILE_UPLOAD

    process_execution_status_response = client.get("/niscm/public/processexecutionstatus")

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0]["processHistoryID"]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0]["fileName"]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0]["processType"] == 1
    assert jsonified_process_execution_status_response[DATA][0]["statusCode"] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0]["statusMessage"]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___connected_to_sle___product_unavailable___return_not_found_response(client: Client):
    products_response = client.get("/niscm/public/products")

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    response = client.get(INVALID_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_NOT_FOUND_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE

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

    process_execution_status_response = client.get("/niscm/public/processexecutionstatus")

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0]["processHistoryID"]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0]["fileName"]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0]["processType"] == 1
    assert jsonified_process_execution_status_response[DATA][0]["statusCode"] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0]["statusMessage"]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___connected_to_sle___invalid_measurement_file___return_server_error_response(
    client: Client,
):
    products_response = client.get("/niscm/public/products")

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    specs_response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_specs_response = specs_response.get_json()

    assert specs_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_specs_response[DATA]) != 0
    assert jsonified_specs_response[STATE] == ScmResponseStateCodes.SUCCESS

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

    process_execution_status_response = client.get("/niscm/public/processexecutionstatus")

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0]["processHistoryID"]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0]["fileName"]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0]["processType"] == 1
    assert jsonified_process_execution_status_response[DATA][0]["statusCode"] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0]["statusMessage"]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS
