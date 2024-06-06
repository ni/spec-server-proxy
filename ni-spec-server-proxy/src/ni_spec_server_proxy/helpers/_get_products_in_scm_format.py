"""Helper functions for converting SLE API Get Products Response to SCM API Get Products Response.""" # noqa W505

from typing import Any, Dict, List

from systemlink.clients.nitestmonitor.models import ProductResponseObject

from ni_spec_server_proxy.constants import ScmResponseStateCodes


PRODUCT_REVISION = "1.0"


def __format_get_products_response_data(
    get_products_response: ProductResponseObject
) -> List[Dict[str, str]]:
    """Format SLE get products response data to SCM get products response data.

    Args:
        get_products_response (ProductResponseObject): SLE get products response.

    Returns:
        List[Dict[str, str]]: SCM get products response.
    """
    scm_get_product_data = []

    for product_data in get_products_response.products:
        scm_get_product_data.append(
            {
                "productName": product_data.part_number,
                "revision": PRODUCT_REVISION
            }
        )

    return scm_get_product_data


def convert_get_products_response(get_products_response: ProductResponseObject) -> Dict[str, Any]:
    """Convert SLE get Products Response to SCM get products response.

    Args:
        get_products_response (ProductResponseObject): SLE get products Response to be converted.

    Returns:
        Dict[str, Any]: Converted get products response.
    """
    return {
        "data": __format_get_products_response_data(get_products_response),
        "message": "All Views fetched successfully",
        "state": ScmResponseStateCodes.SUCCESS
    }
