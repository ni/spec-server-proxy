"""Implementation of flask server to use SCM API end points."""

import os

import pandas as pd
import systemlink.clients.nitestmonitor as testmon
from flask import Flask, Response, jsonify, request
from nisystemlink.clients.core import HttpConfigurationManager
from nisystemlink.clients.spec import SpecClient
from systemlink.clients.nitestmonitor.models import ProductsAdvancedQuery

from ni_spec_server_proxy.constants import (
    CHIP_ID_COLUMN,
    CHIP_ID_INDEX,
    EMPTY_VALUE,
    FILE_NAME_KEY,
    META,
    PROCESS_HISTORY_ID_KEY,
    TEST_BENCH_COLUMN,
    FileUpload,
    ProcessExecutionResponse,
    ResponseField,
    ScmResponseStateCodes,
    StatusCode,
)
from ni_spec_server_proxy.helpers import (
    convert_get_products_response,
    get_error_response,
    get_minion_id,
    get_query_specs_response,
    handle_errors,
    upload_file_to_part_number,
)

TAKE_COUNT = 1000
spec_client = SpecClient(configuration=HttpConfigurationManager.get_configuration())

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """Home page of the Proxy server.

    Returns:
        str: SCM Proxy server welcome message.
    """
    res = "Welcome to Proxy NI SCM Spec Server! Please redirect to your desired endpoint."
    return res


@app.route("/niscm/public/products", methods=["GET"])
@handle_errors("An error occured while getting SLE Products")
async def get_products() -> Response:
    """Getting SLE products in SCM Response format.

    Returns:
        Response: Get products response.
    """
    testmon_api_client = testmon.ApiClient()
    products_api = testmon.ProductsApi(testmon_api_client)
    try:
        response = await products_api.get_products_v2(take=TAKE_COUNT)
        response = convert_get_products_response(response)
        return jsonify(response)

    finally:
        await products_api.api_client.close()
        await testmon_api_client.close()


@app.route("/niscm/public/spec/<product_name>/<product_revision>", methods=["GET"])
@handle_errors("An error occured while getting specs data")
async def get_specs(product_name: str, product_revision: str) -> Response:
    """Getting specs from SLE Product in SCM Response format.

    Args:
        product_name (str): Part Number of the product.
        product_revision (str): Product revision.

    Returns:
        Response: Get specs response.
    """
    testmon_api_client = testmon.ApiClient()
    products_api = testmon.ProductsApi(testmon_api_client)

    query_product_request_body = ProductsAdvancedQuery(
        filter=f'(partNumber == "{product_name}")',
    )
    try:
        query_product_response = await products_api.query_products_v2(
            post_body=query_product_request_body
        )

        if not query_product_response.products:
            response = get_error_response(
                status_code=StatusCode.NOT_FOUND,
                error_message="Invalid Product",
            )

        else:
            product_id = query_product_response.products[0].id
            response = get_query_specs_response(product_id=product_id, spec_client=spec_client)
            response = jsonify(response)

        return response

    finally:
        await products_api.api_client.close()
        await testmon_api_client.close()


@app.route(
    "/niscm/public/data/upload/<product_name>/<product_revision>/<discipline>",
    methods=["POST"],
)
@handle_errors("An error occurred in measurement file upload.")
async def upload_measurement(product_name: str, product_revision: str, discipline: str) -> Response:
    """Upload measurement file to SLE workspace and link it to the product using part number.

    Args:
        product_name (str): Part Number of product.
        product_revision (str): Product revision.
        discipline (str): File uploaded to `discipline`.

    Returns:
        Response: Defaults to success response.
    """
    os.makedirs(FileUpload.DIRECTORY, exist_ok=True)
    file = request.files[FileUpload.FORM_COLLECTION]

    # FileName format:
    # [StationID][SequenceFile][Data][Time][BatchSerialNumber][UUTSerialNumber][TestSocket].csv
    splitted_file_name = file.filename.split("]")

    file_name = file.filename.replace("[", "")
    file_name = file_name.replace("]", "_")
    file_path = os.path.join(FileUpload.DIRECTORY, file_name)
    file.seek(0)
    file.save(file_path)

    measurement_df = pd.read_csv(file_path, encoding="latin1", header=0)
    # Add `TestBench` column.
    measurement_df.insert(0, TEST_BENCH_COLUMN, EMPTY_VALUE)
    measurement_df.at[0, TEST_BENCH_COLUMN] = META
    minion_id = get_minion_id()
    measurement_df.loc[1:, TEST_BENCH_COLUMN] = minion_id

    # Add `ChipId` column.
    measurement_df.insert(0, CHIP_ID_COLUMN, EMPTY_VALUE)
    measurement_df.at[0, CHIP_ID_COLUMN] = META

    # Check if UUT Serial Number is present.
    if len(splitted_file_name) > 6:
        measurement_df.loc[1:, CHIP_ID_COLUMN] = splitted_file_name[CHIP_ID_INDEX][1:]

    measurement_df.to_csv(file_path, index=False)

    response = await upload_file_to_part_number(
        file_path=file_path,
        part_number=product_name,
    )

    if response is None or response.error is not None:
        error_response = get_error_response(
            error_message="Invalid Product",
            status_code=StatusCode.NOT_FOUND,
        )
        return error_response

    success_response = {
        ResponseField.DATA: {
            FILE_NAME_KEY: file_name,
            PROCESS_HISTORY_ID_KEY: FileUpload.PROCESS_HISTORY_ID,
            "errors": [],
        },
        ResponseField.MESSAGE: FileUpload.SUCCESS_MESSAGE,
        ResponseField.STATE: ScmResponseStateCodes.SUCCESS,
    }
    return jsonify(success_response)


@app.route("/niscm/public/processexecutionstatus", methods=["GET"])
@handle_errors("An error occurred in get process execution status.")
async def get_process_execution_status() -> Response:
    """Get process execution status.

    Return success message by default in order to send response to measurement file upload's \
        follow up get process execution status request.

    Returns:
        Response: Defaults to success response always.
    """
    response = ProcessExecutionResponse.SUCCESS_RESPONSE
    return jsonify(response)


async def run():
    """Flask server."""
    app.run(host="0.0.0.0", port=8000)
