"""Contains test case to validate valid workflow."""

from typing import Callable

from werkzeug import Client

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from ni_spec_server_proxy.main import TAKE_COUNT
from tests.constants import (
    DATA,
    ERRORS,
    FILENAME,
    GET_PROCESS_EXECUTION_STATUS_URL,
    GET_PRODUCTS_URL,
    INVALID_MEASUREMENT_FILE_PATH,
    INVALID_PRODUCT_GET_SPEC_URL,
    INVALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
    MESSAGE,
    MULTIPART_CONTENT,
    PROCESS_HISTORY_ID,
    PROCESS_TYPE,
    STATE,
    STATUS_CODE,
    STATUS_INTERNAL_SERVER_RESPONSE_CODE,
    STATUS_MESSAGE,
    STATUS_NOT_FOUND_RESPONSE_CODE,
    STATUS_SUCCESS_RESPONSE_CODE,
    SUCCESS_STATE_IN_FILE_UPLOAD,
    VALID_MEASUREMENT_FILE_NAME,
    VALID_MEASUREMENT_FILE_PATH,
    VALID_PRODUCT_GET_SPEC_URL,
    VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
)


def test___connected_to_sle___product_available____returns_success_response(
    client: Client,
    get_upload_measurement_data: Callable,
):
    products_response = client.get(GET_PRODUCTS_URL)

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    specs_response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_specs_response = specs_response.get_json()

    assert specs_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_specs_response[DATA]) != 0
    assert jsonified_specs_response[STATE] == ScmResponseStateCodes.SUCCESS

    upload_data = get_upload_measurement_data(file_path=VALID_MEASUREMENT_FILE_PATH)

    file_upload_response = client.post(
        VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=upload_data,
        content_type=MULTIPART_CONTENT,
    )

    jsonified_file_upload_response = file_upload_response.get_json()

    assert file_upload_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert jsonified_file_upload_response[DATA][FILENAME] == VALID_MEASUREMENT_FILE_NAME
    assert not jsonified_file_upload_response[DATA][ERRORS]
    assert jsonified_file_upload_response[STATE] == SUCCESS_STATE_IN_FILE_UPLOAD

    process_execution_status_response = client.get(GET_PROCESS_EXECUTION_STATUS_URL)

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0][PROCESS_HISTORY_ID]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0][FILENAME]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0][PROCESS_TYPE] == 1
    assert jsonified_process_execution_status_response[DATA][0][STATUS_CODE] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0][STATUS_MESSAGE]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___connected_to_sle___product_unavailable___return_product_not_found(
    client: Client,
    get_upload_measurement_data: Callable,
):
    products_response = client.get(GET_PRODUCTS_URL)

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    response = client.get(INVALID_PRODUCT_GET_SPEC_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_NOT_FOUND_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE

    upload_data = get_upload_measurement_data(file_path=VALID_MEASUREMENT_FILE_PATH)

    response = client.post(
        INVALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=upload_data,
        content_type=MULTIPART_CONTENT,
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_NOT_FOUND_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE

    process_execution_status_response = client.get(GET_PROCESS_EXECUTION_STATUS_URL)

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0][PROCESS_HISTORY_ID]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0][FILENAME]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0][PROCESS_TYPE] == 1
    assert jsonified_process_execution_status_response[DATA][0][STATUS_CODE] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0][STATUS_MESSAGE]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS


def test___connected_to_sle___invalid_measurement_file___return_internal_server_error(
    client: Client,
    get_upload_measurement_data: Callable,
):
    products_response = client.get(GET_PRODUCTS_URL)

    jsonified_products_response = products_response.get_json()

    assert products_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_products_response[DATA]) <= TAKE_COUNT
    assert jsonified_products_response[STATE] == ScmResponseStateCodes.SUCCESS

    specs_response = client.get(VALID_PRODUCT_GET_SPEC_URL)

    jsonified_specs_response = specs_response.get_json()

    assert specs_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert len(jsonified_specs_response[DATA]) != 0
    assert jsonified_specs_response[STATE] == ScmResponseStateCodes.SUCCESS

    upload_data = get_upload_measurement_data(file_path=INVALID_MEASUREMENT_FILE_PATH)

    response = client.post(
        VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=upload_data,
        content_type=MULTIPART_CONTENT,
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_INTERNAL_SERVER_RESPONSE_CODE
    assert not jsonified_response[DATA]
    assert jsonified_response[STATE] == ScmResponseStateCodes.FAILURE

    process_execution_status_response = client.get(GET_PROCESS_EXECUTION_STATUS_URL)

    jsonified_process_execution_status_response = process_execution_status_response.get_json()

    assert process_execution_status_response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert (
        jsonified_process_execution_status_response[DATA][0][PROCESS_HISTORY_ID]
        == FileUpload.PROCESS_HISTORY_ID
    )
    assert (
        jsonified_process_execution_status_response[DATA][0][FILENAME]
        == FileUpload.DEFAULT_FILE_NAME
    )
    assert jsonified_process_execution_status_response[DATA][0][PROCESS_TYPE] == 1
    assert jsonified_process_execution_status_response[DATA][0][STATUS_CODE] == 1
    assert (
        jsonified_process_execution_status_response[DATA][0][STATUS_MESSAGE]
        == FileUpload.SUCCESS_MESSAGE
    )
    assert jsonified_process_execution_status_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_process_execution_status_response[STATE] == ScmResponseStateCodes.SUCCESS
