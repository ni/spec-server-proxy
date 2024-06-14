"""Upload a file to SLE and link it to a product."""

from typing import Union

import systemlink.clients.nifile as file
import systemlink.clients.nitestmonitor as testmon
from systemlink.clients.nitestmonitor.models.error_response import ErrorResponse
from systemlink.clients.nitestmonitor.models.products_partial_success_response import (
    ProductsPartialSuccessResponse,
)

from ni_spec_server_proxy.helpers._get_workspace_id import get_system_workspace

system_workspace_id = get_system_workspace()  # Get workspace ID from SystemLink Client.


async def upload_file(
    file_path: str,
    files_api: file.FilesApi,
    workspace: str = system_workspace_id,
) -> str:
    """Upload a file to workspace.

    Args:
        file_path (str): File path.
        files_api (file.FilesApi): File client object.
        workspace (str, optional): Workspace ID. Defaults to `system_workspace_id`.

    Returns:
        str: ID of file being uploaded.
    """
    response = await files_api.upload(file=file_path, workspace=workspace)
    file_id = response.uri.split("/")[-1]
    return file_id


async def get_product_id(part_number: str, products_api: testmon.ProductsApi) -> Union[str, None]:
    """Get product id using part number of the product.

    Args:
        part_number (str): Part number of SLE product.
        products_api (testmon.ProductsApi): Product client object.

    Returns:
        Union[str, None]: ID of SLE product. If no product found, returns None.
    """
    query = testmon.ProductValuesQuery(
        field=testmon.ProductField.ID,
        filter=f'partNumber == "{part_number}"',
    )
    products = await products_api.query_product_values_v2(query)

    if products:
        return products[0]
    else:
        return None


async def link_file_to_product(
    file_id: str,
    product_id: str,
    products_api: testmon.ProductsApi,
) -> Union[ProductsPartialSuccessResponse, ErrorResponse]:
    """Link file to a product.

    Args:
        file_id (str): ID of uploaded file.
        product_id (str): ID of SLE product.
        products_api (testmon.ProductsApi): Product client object.

    Returns:
        Union[ProductsPartialSuccessResponse, ErrorResponse]: Response of `update_products_v2`.
    """
    update_product_request = testmon.ProductUpdateRequestObject(file_ids=[file_id], id=product_id)
    request = testmon.UpdateProductsRequest(products=[update_product_request], replace=False)
    response = await products_api.update_products_v2(request_body=request)
    return response


async def __upload_file_to_part_number(
    file_path: str,
    part_number: str,
    files_api: file.ApiClient,
    products_api: testmon.ApiClient,
) -> Union[ProductsPartialSuccessResponse, ErrorResponse, None]:

    file_id = await upload_file(file_path=file_path, files_api=files_api)
    product_id = await get_product_id(part_number=part_number, products_api=products_api)

    if product_id is not None:
        updated_product = await link_file_to_product(
            file_id=file_id,
            product_id=product_id,
            products_api=products_api,
        )
        return updated_product

    return product_id


async def upload_file_to_part_number(
    file_path: str,
    part_number: str,
) -> Union[ProductsPartialSuccessResponse, ErrorResponse, None]:
    """Upload a file to SLE and link to a product.

    Args:
        file_path (str): File path.
        part_number (str): Part number of SLE product.

    Returns:
        Union[ProductsPartialSuccessResponse, ErrorResponse, None]: Response of \
            `update_products_v2` or None.
    """
    file_api_client = file.ApiClient()
    testmon_api_client = testmon.ApiClient()

    files_api = file.FilesApi(file_api_client)
    products_api = testmon.ProductsApi(testmon_api_client)

    try:
        response = await __upload_file_to_part_number(
            file_path,
            part_number,
            files_api,
            products_api,
        )
        return response
    finally:
        await files_api.api_client.close()
        await products_api.api_client.close()

        await file_api_client.close()
        await testmon_api_client.close()
