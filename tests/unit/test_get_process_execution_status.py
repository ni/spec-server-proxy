"""Contains tests to validate get_process_execution_status API."""

from werkzeug.test import Client

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from tests.constants import (
    DATA,
    FILENAME,
    GET_PROCESS_EXECUTION_STATUS_URL,
    MESSAGE,
    PROCESS_HISTORY_ID,
    PROCESS_TYPE,
    STATE,
    STATUS_CODE,
    STATUS_MESSAGE,
    STATUS_SUCCESS_RESPONSE_CODE,
)


def test___get_process_execution_status___returns_success_response(client: Client) -> None:
    response = client.get(GET_PROCESS_EXECUTION_STATUS_URL)

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS_RESPONSE_CODE
    assert jsonified_response[DATA][0][PROCESS_HISTORY_ID] == FileUpload.PROCESS_HISTORY_ID
    assert jsonified_response[DATA][0][FILENAME] == FileUpload.DEFAULT_FILE_NAME
    assert jsonified_response[DATA][0][PROCESS_TYPE] == 1
    assert jsonified_response[DATA][0][STATUS_CODE] == 1
    assert jsonified_response[DATA][0][STATUS_MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS
