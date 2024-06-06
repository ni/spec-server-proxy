"""Constants utilized in file upload to SLE."""

from ni_spec_server_proxy.constants import ResponseField, ScmResponseStateCodes

FILE_NAME_KEY = "fileName"
PROCESS_HISTORY_ID_KEY = "processHistoryID"

META = "META"
CHIP_ID_COLUMN = "ChipId"
TEST_BENCH_COLUMN = "TestBench"

EMPTY_VALUE = ""
CHIP_ID_INDEX = -3


class FileUpload:
    """File Upload Constants."""

    FORM_COLLECTION = "formCollection"
    DEFAULT_FILE_NAME = "measurement.csv"
    PROCESS_HISTORY_ID = 12345  # Some random value since in SLE we don't have Process History ID.
    SUCCESS_MESSAGE = "File uploaded successfully."


class ProcessExecutionResponse:
    """Process Execution Status Constants."""

    _SUCCESS_STATE_CODE = 1
    _PROCESS_TYPE_CODE = 1  # For measurement file upload.

    SUCCESS_RESPONSE = {
        ResponseField.DATA: [
            {
                PROCESS_HISTORY_ID_KEY: FileUpload.PROCESS_HISTORY_ID,
                FILE_NAME_KEY: FileUpload.DEFAULT_FILE_NAME,
                "processType": _PROCESS_TYPE_CODE,
                "statusCode": _SUCCESS_STATE_CODE,
                "statusMessage": FileUpload.SUCCESS_MESSAGE,
            }
        ],
        ResponseField.MESSAGE: FileUpload.SUCCESS_MESSAGE,
        ResponseField.STATE: ScmResponseStateCodes.SUCCESS,
    }
