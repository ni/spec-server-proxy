"""Contains tests to validate get_process_execution_status API."""

from werkzeug.test import Client

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from tests.constants import DATA, MESSAGE, STATE, STATUS_SUCCESS


def test___get_process_execution_status___returns_success_response(client: Client):
    response = client.get("/niscm/public/processexecutionstatus")

    jsonified_response = response.get_json()

    assert response.status_code == STATUS_SUCCESS
    assert jsonified_response[DATA][0]["processHistoryID"] == FileUpload.PROCESS_HISTORY_ID
    assert jsonified_response[DATA][0]["fileName"] == FileUpload.DEFAULT_FILE_NAME
    assert jsonified_response[DATA][0]["processType"] == 1
    assert jsonified_response[DATA][0]["statusCode"] == 1
    assert jsonified_response[DATA][0]["statusMessage"] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_response[MESSAGE] == FileUpload.SUCCESS_MESSAGE
    assert jsonified_response[STATE] == ScmResponseStateCodes.SUCCESS
