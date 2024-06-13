"""Unit test for get condition mappings in SCM response from SLE API response."""

from typing import List

import pytest
from nisystemlink.clients.spec.models import (
    Condition,
    ConditionRange,
    ConditionType,
    NumericConditionValue,
    StringConditionValue,
)

from ni_spec_server_proxy.helpers import get_condition_response_mappings

_COLUMN_NAME = "columnName"
_COLUMN_VALUE = "columnValue"


@pytest.fixture(scope="class")
def get_condition_data_with_no_unit() -> List[Condition]:
    """Fixture to get condition data with no unit."""
    condition_data_with_no_unit = [
        Condition(
            name="Temperature",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[],
                discrete=[4.0],
                unit=None,
            ),
        )
    ]
    return condition_data_with_no_unit


@pytest.fixture(scope="class")
def get_condition_data_with_unit() -> List[Condition]:
    """Fixture to get condition data with unit."""
    condition_data_with_unit = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=0, max=9.0, step=3.0)],
                discrete=[3.0, 6.0],
                unit="V",
            ),
        )
    ]
    return condition_data_with_unit


@pytest.fixture(scope="class")
def get_condition_data_with_string_values() -> List[Condition]:
    """Fixture to get condition data with string type."""
    string_condition_data = [
        Condition(
            name="Process Corners",
            value=StringConditionValue(
                condition_type=ConditionType.STRING, discrete=["TT", "FS", "SS", "SF"]
            ),
        )
    ]
    return string_condition_data


@pytest.fixture(scope="class")
def get_condition_data_with_single_string_data() -> List[Condition]:
    """Fixture to get condition data with single string data."""
    string_condition_data = [
        Condition(
            name="Process Corners",
            value=StringConditionValue(condition_type=ConditionType.STRING, discrete=["TT"]),
        )
    ]
    return string_condition_data


@pytest.fixture(scope="class")
def get_condition_data_with_no_lower_limit() -> List[Condition]:
    """Fixture to get condition data with no lower limit."""
    condition_data_with_no_lower_limit = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=None, max=9.0, step=3.0)],
                discrete=[3.0, 6.0],
                unit="V",
            ),
        )
    ]
    return condition_data_with_no_lower_limit


@pytest.fixture(scope="class")
def get_condition_data_with_no_upper_limit() -> List[Condition]:
    """Fixture to get condition data with no upper limit."""
    condition_data_with_no_upper_limit = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=0, max=None, step=3.0)],
                discrete=[3.0, 6.0],
                unit="V",
            ),
        )
    ]
    return condition_data_with_no_upper_limit


@pytest.fixture(scope="class")
def get_condition_data_with_no_range() -> List[Condition]:
    """Fixture to get condition data with no range."""
    condition_data_with_no_range = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=None,
                discrete=[4.0],
                unit=None,
            ),
        )
    ]
    return condition_data_with_no_range


@pytest.fixture(scope="class")
def get_condition_data_with_range() -> List[Condition]:
    """Fixture to get condition data with range."""
    condition_data_with_range = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=0, max=9.0, step=3.0)],
                discrete=[3.0, 6.0],
                unit="V",
            ),
        )
    ]
    return condition_data_with_range


@pytest.fixture(scope="class")
def get_condition_data_with_only_limits() -> List[Condition]:
    """Fixture to get condition data with only limits."""
    condition_data_with_only_limits = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=0, max=9.0, step=None)],
                discrete=[],
                unit="V",
            ),
        )
    ]
    return condition_data_with_only_limits


@pytest.fixture(scope="class")
def get_condition_data_with_only_upper_limit() -> List[Condition]:
    """Fixture to get condition data with only upper limit."""
    condition_data_with_only_upper_limit = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=None, max=9.0, step=None)],
                discrete=[],
                unit="V",
            ),
        )
    ]
    return condition_data_with_only_upper_limit


@pytest.fixture(scope="class")
def get_condition_data_with_only_lower_limit() -> List[Condition]:
    """Fixture to get condition data with only lower limit."""
    condition_data_with_only_lower_limit = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=[ConditionRange(min=0, max=None, step=None)],
                discrete=[],
                unit="V",
            ),
        )
    ]
    return condition_data_with_only_lower_limit


@pytest.fixture(scope="class")
def get_condition_data_for_numeric_values() -> List[Condition]:
    """Fixture to get condition data with list of numeric values."""
    condition_data_with_numeric_data = [
        Condition(
            name="Vsys",
            value=NumericConditionValue(
                condition_type=ConditionType.NUMERIC,
                range=None,
                discrete=[1, 2, 3],
                unit="V",
            ),
        )
    ]
    return condition_data_with_numeric_data


class TestConditionResponse:
    """Unit test for get condition mapping response function."""

    def test__get_condition_mappings_response_without_range(
        self,
        get_condition_data_with_no_range: List[Condition],
    ):
        """Test get condition mapping response without range."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_no_range
        )
        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys",
                _COLUMN_VALUE: "[4]",
            },
        ]

    def test__get_condition_mappings_response_with_range(
        self,
        get_condition_data_with_range: List[Condition],
    ):
        """Test get condition mapping response with range."""
        condition_mapping_response = get_condition_response_mappings(get_condition_data_with_range)
        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[0..3..6..9]",
            },
        ]

    def test__get_condition_mappings_response_with_unit(
        self,
        get_condition_data_with_unit: List[Condition],
    ):
        """Test get condition mapping response with unit."""
        condition_mapping_response = get_condition_response_mappings(get_condition_data_with_unit)
        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[0..3..6..9]",
            },
        ]

    def test__get_condition_mappings_response_with_no_unit(
        self,
        get_condition_data_with_no_unit: List[Condition],
    ):
        """Test get condition mapping response with no unit."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_no_unit
        )
        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Temperature",
                _COLUMN_VALUE: "[4]",
            },
        ]

    def test_get_condition_mappings_response_with_no_upper_limit(
        self,
        get_condition_data_with_no_upper_limit: List[Condition],
    ):
        """Test get condition mapping response with no upper limit in range."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_no_upper_limit
        )
        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[0..3..6..]",
            },
        ]

    def test_get_condition_mappings_response_with_no_lower_limit(
        self,
        get_condition_data_with_no_lower_limit: List[Condition],
    ):
        """Test get condition mapping response with no lower limit in range."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_no_lower_limit
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[..3..6..9]",
            },
        ]

    def test_get_condition_mappings_response_with_string_data(
        self,
        get_condition_data_with_string_values: List[Condition],
    ):
        """Test get condition mapping response with string data."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_string_values
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Process Corners",
                _COLUMN_VALUE: "TT,FS,SS,SF",
            },
        ]

    def test_get_condition_mappings_response_with_only_limits(
        self,
        get_condition_data_with_only_limits: List[Condition],
    ):
        """Test get condition mapping response which has only limit values."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_only_limits
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[0..9]",
            },
        ]

    def test_get_condition_mappings_response_for_numeric_data(
        self,
        get_condition_data_for_numeric_values: List[Condition],
    ):
        """Test get condition mapping response for list of numeric values."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_for_numeric_values
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[1,2,3]",
            },
        ]

    def test_get_condition_mappings_response_for_single_string_value(
        self,
        get_condition_data_with_single_string_data: List[Condition],
    ):
        """Test get condition mapping response for single string value."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_single_string_data
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Process Corners",
                _COLUMN_VALUE: "TT",
            },
        ]

    def test_get_condition_mappings_response_with_only_upper_limit(
        self,
        get_condition_data_with_only_upper_limit: List[Condition],
    ):
        """Test get condition mapping response which has only upper limit value."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_only_upper_limit
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[..9]",
            },
        ]

    def test_get_condition_mappings_response_with_only_lower_limit(
        self,
        get_condition_data_with_only_lower_limit: List[Condition],
    ):
        """Test get condition mapping response which has only lower limit value."""
        condition_mapping_response = get_condition_response_mappings(
            get_condition_data_with_only_lower_limit
        )

        assert condition_mapping_response == [
            {
                _COLUMN_NAME: "Vsys (V)",
                _COLUMN_VALUE: "[0..]",
            },
        ]
