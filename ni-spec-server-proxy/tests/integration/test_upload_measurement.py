"""Contains tests to validate the upload_measurement feature."""

import io

from werkzeug import Client
from werkzeug.datastructures import FileStorage

from ni_spec_server_proxy.constants import FileUpload, ScmResponseStateCodes
from tests.constants import (
    DATA,
    DISCIPLINE,
    MESSAGE,
    STATE,
    STATUS_SUCCESS_RESPONSE_CODE,
    SUCCESS_STATE_IN_FILE_UPLOAD,
    VALID_MEASUREMENT_FILE_NAME,
    VALID_MEASUREMENT_FILE_PATH,
    VALID_PRODUCT_NAME,
    VALID_PRODUCT_REVISION,
)


def test___upload_measurement_process_execution_status___returns_success_response(client: Client):
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
