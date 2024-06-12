"""Constants utilized in the test cases."""

import os

DATA = "data"
STATE = "state"
MESSAGE = "message"
ERRORS = "errors"

PROCESS_HISTORY_ID = "processHistoryID"
FILENAME = "fileName"
PROCESS_TYPE = "processType"
STATUS_CODE = "statusCode"
STATUS_MESSAGE = "statusMessage"
DISCIPLINE = "Validation"

STATUS_SUCCESS_RESPONSE_CODE = 200
STATUS_NOT_FOUND_RESPONSE_CODE = 404
STATUS_INTERNAL_SERVER_RESPONSE_CODE = 500
SUCCESS_STATE_IN_FILE_UPLOAD = 0

VALID_PRODUCT_NAME = "GR_PWA"  # Valid product with specs.
NO_SPEC_PRODUCT_NAME = "Test partnumber"  # Valid product without specs.
VALID_PRODUCT_REVISION = "1.0"

INVALID_PRODUCT_NAME = "INVALID PRODUCT"

GET_PRODUCTS_URL = "/niscm/public/products"
GET_PROCESS_EXECUTION_STATUS_URL = "/niscm/public/processexecutionstatus"

MULTIPART_CONTENT = "multipart/form-data"

VALID_PRODUCT_UPLOAD_MEASUREMENT_URL = (
    f"/niscm/public/data/upload/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}"
)
INVALID_PRODUCT_UPLOAD_MEASUREMENT_URL = (
    f"/niscm/public/data/upload/{INVALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}/{DISCIPLINE}"
)

VALID_PRODUCT_GET_SPEC_URL = f"/niscm/public/spec/{VALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}"
INVALID_PRODUCT_GET_SPEC_URL = f"/niscm/public/spec/{INVALID_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}"
NO_SPEC_PRODUCT_GET_SPEC_URL = f"/niscm/public/spec/{NO_SPEC_PRODUCT_NAME}/{VALID_PRODUCT_REVISION}"

# Replace valid_measurement.csv with suitable measurements.
VALID_MEASUREMENT_FILE_NAME = "valid_measurement.csv"
VALID_MEASUREMENT_FILE_PATH = os.path.join(
    os.getcwd(),
    "tests",
    "assets",
    VALID_MEASUREMENT_FILE_NAME,
)

INVALID_MEASUREMENT_FILE_NAME = "invalid_measurement.csv"
INVALID_MEASUREMENT_FILE_PATH = os.path.join(
    os.getcwd(),
    "tests",
    "assets",
    INVALID_MEASUREMENT_FILE_NAME,
)
