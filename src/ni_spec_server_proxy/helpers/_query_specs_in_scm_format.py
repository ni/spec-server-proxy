"""Helper functions for Fetching and converting SLE API Query Specs Response to SCM API Get Specs Response."""  # noqa: W505

from typing import Dict, List, TypedDict, Union

from nisystemlink.clients.spec import SpecClient
from nisystemlink.clients.spec.models import (
    Condition,
    ConditionType,
    NumericConditionValue,
    QuerySpecifications,
    QuerySpecificationsRequest,
)

from ni_spec_server_proxy.constants import (
    RANGE_SPECIFIER,
    LimitParams,
    ScmGetSpecsResponse,
    ScmResponseStateCodes,
    ScmStdColumns,
)

TAKE_COUNT = 1000


class SCMSpecResponse(TypedDict):
    """SCM Spec Response Dictionary."""

    data: List[Dict[str, Union[str, int, float, None, List[Dict[str, str]]]]]
    message: str
    state: int


def __parse_value(value: Union[int, float, str]) -> Union[int, float, str]:
    """Parse value to possible data type.

    Args:
        value (Union[int, float, str]): Value to be parsed.

    Returns:
        Union[int, float, str]: Parsed value.
    """
    try:
        result = float(value)
        if result.is_integer():
            return int(result)

        return result

    except ValueError:
        return str(value)


def get_condition_response_mappings(spec_conditions: List[Condition]) -> List[Dict[str, str]]:
    """Get Condition Response Mappings of SCM get specs API.

    Args:
        spec_conditions (List[Condition]): SLE Query Specs condition response.

    Returns:
        List[Dict[str, str]]: SCM spec condition data.
    """
    condition_response_mapping = []

    for cond_data in spec_conditions:
        if cond_data.name is None:
            continue

        converted_cond_data: Dict[str, str] = {
            ScmGetSpecsResponse.COLUMN_NAME: cond_data.name,
            ScmGetSpecsResponse.COLUMN_VALUE: "",
        }

        if cond_data.value is None or cond_data.value.discrete is None:
            condition_response_mapping.append(converted_cond_data)
            continue

        if (
            isinstance(cond_data.value, NumericConditionValue)
            and cond_data.value.condition_type == ConditionType.NUMERIC
            and cond_data.value.unit is not None
        ):
            converted_cond_data[ScmGetSpecsResponse.COLUMN_NAME] += (
                " (" + cond_data.value.unit + ")"
            )

        converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] = ",".join(
            [(str(__parse_value(val))) for val in cond_data.value.discrete]
        )

        if (
            isinstance(cond_data.value, NumericConditionValue)
            and cond_data.value.condition_type == ConditionType.NUMERIC
            and not cond_data.value.range
        ):
            converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] = (
                "["
                + str(__parse_value(converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE]))
                + "]"
            )

        elif (
            isinstance(cond_data.value, NumericConditionValue)
            and cond_data.value.condition_type == ConditionType.NUMERIC
            and cond_data.value.range
        ):
            converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] = "["

            if cond_data.value.range[0].min is None:
                converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += RANGE_SPECIFIER
            else:
                converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += str(
                    __parse_value(cond_data.value.range[0].min)
                )
                if cond_data.value.discrete or cond_data.value.range[0].max:
                    converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += RANGE_SPECIFIER

            converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += RANGE_SPECIFIER.join(
                [(str(__parse_value(val))) for val in cond_data.value.discrete]
            )

            if cond_data.value.range[0].max is None:
                converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += RANGE_SPECIFIER

            else:
                if cond_data.value.discrete:
                    converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += RANGE_SPECIFIER

                converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += str(
                    __parse_value(cond_data.value.range[0].max)
                )

            converted_cond_data[ScmGetSpecsResponse.COLUMN_VALUE] += "]"

        condition_response_mapping.append(converted_cond_data)

    return condition_response_mapping


def get_info_response_mappings(spec_info_data: Dict[str, str]) -> List[Dict[str, str]]:
    """Get spec info response mappings of SCM get specs API.

    Args:
        spec_info_data (Dict[str, str]): Spec information data from query specs API.

    Returns:
        List[Dict[str, str]]: SCM spec information data.
    """
    info_response_mappings = []
    for info_col, info_val in spec_info_data.items():
        info_response_mappings.append(
            {
                ScmGetSpecsResponse.COLUMN_NAME: info_col,
                ScmGetSpecsResponse.COLUMN_VALUE: info_val,
            }
        )

    return info_response_mappings


def convert_query_specs_response(query_specs_response: QuerySpecifications) -> SCMSpecResponse:
    """Convert query specs response to SCM Response format.

    Args:
        query_specs_response (QuerySpecifications): Query Specs Response.

    Returns:
        SCMSpecResponse: Converted SCM Response.
    """
    scm_get_specs_response: SCMSpecResponse = {
        "data": [],
        "message": "All Views fetched successfully",
        "state": ScmResponseStateCodes.SUCCESS,
    }

    if query_specs_response.specs is None:
        return scm_get_specs_response

    count = 0
    for spec_data in query_specs_response.specs:
        formatted_spec_data: Dict[str, Union[str, int, float, None, List[Dict[str, str]]]] = {
            "id": count
        }
        count += 1

        formatted_spec_data[ScmStdColumns.SPEC_ID] = spec_data.spec_id
        formatted_spec_data[ScmStdColumns.SYMBOL] = spec_data.symbol
        formatted_spec_data[ScmStdColumns.BLOCK] = spec_data.block
        formatted_spec_data[ScmStdColumns.CATEGORY] = spec_data.category
        formatted_spec_data[ScmStdColumns.UNIT] = spec_data.unit
        formatted_spec_data[ScmStdColumns.NAME] = spec_data.name

        if spec_data.limit is not None:
            formatted_spec_data[LimitParams.TYPICAL] = spec_data.limit.typical
            formatted_spec_data[LimitParams.MIN] = spec_data.limit.min
            formatted_spec_data[LimitParams.MAX] = spec_data.limit.max
        else:
            formatted_spec_data[LimitParams.TYPICAL] = None
            formatted_spec_data[LimitParams.MIN] = None
            formatted_spec_data[LimitParams.MAX] = None

        if spec_data.properties:
            formatted_spec_data[ScmGetSpecsResponse.INFO] = get_info_response_mappings(
                spec_data.properties
            )

        if spec_data.conditions:
            formatted_spec_data[ScmGetSpecsResponse.CONDITIONS] = get_condition_response_mappings(
                spec_data.conditions
            )
        scm_get_specs_response["data"].append(formatted_spec_data)

    return scm_get_specs_response


def get_query_specs_response(product_id: str, spec_client: SpecClient) -> SCMSpecResponse:
    """Get SLE query specs response.

    Args:
        product_id (str): Id of the product.
        spec_client: (SpecClient): Spec Client object for getting specs.

    Returns:
        SCMSpecResponse: Query specs response in SCM format.
    """
    query_specs_request_body = QuerySpecificationsRequest(
        product_ids=[product_id],
        take=TAKE_COUNT,
    )
    query_specs_response = spec_client.query_specs(query=query_specs_request_body)
    converted_query_specs_response = convert_query_specs_response(query_specs_response)
    continuation_token = query_specs_response.continuation_token

    while continuation_token:
        query_specs_request_body = QuerySpecificationsRequest(
            product_ids=[product_id],
            take=TAKE_COUNT,
            continuation_token=continuation_token,
        )
        response = spec_client.query_specs(query=query_specs_request_body)
        converted_response_format = convert_query_specs_response(response)

        if converted_response_format["data"]:
            converted_query_specs_response["data"].extend(converted_response_format["data"])

        continuation_token = response.continuation_token

    return converted_query_specs_response
