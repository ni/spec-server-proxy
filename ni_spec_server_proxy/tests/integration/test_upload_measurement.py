"""Contains tests to validate the upload_measurement feature."""

from typing import Callable

from werkzeug import Client

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from tests.constants import (
    DATA,
    ERRORS,
    FILENAME,
    GET_PROCESS_EXECUTION_STATUS_URL,
    INVALID_MEASUREMENT_FILE_PATH,
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
    VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
)


def test___valid_measurement_file___upload_measurement___returns_success_response(
    client: Client,
    get_upload_measurement_data: Callable,
):
    data = get_upload_measurement_data(file_path=VALID_MEASUREMENT_FILE_PATH)

    response = client.post(
        VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=data,
        content_type=MULTIPART_CONTENT,
    )

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert jsonified_response[DATA][FILENAME] == VALID_MEASUREMENT_FILE_NAME
    assert not jsonified_response[DATA][ERRORS]
    assert jsonified_response[STATE] == SUCCESS_STATE_IN_FILE_UPLOAD

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


def test___invalid_measurement_file___upload_measurement___returns_internal_server_error(
    client: Client,
    get_upload_measurement_data: Callable,
):
    data = get_upload_measurement_data(file_path=INVALID_MEASUREMENT_FILE_PATH)

    response = client.post(
        VALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=data,
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


def test___invalid_product___upload_measurement___returns_product_not_found(
    client: Client,
    get_upload_measurement_data: Callable,
):
    data = get_upload_measurement_data(file_path=VALID_MEASUREMENT_FILE_PATH)

    response = client.post(
        INVALID_PRODUCT_UPLOAD_MEASUREMENT_URL,
        data=data,
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
