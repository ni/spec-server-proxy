"""Constants utilized in the get specs end point response conversion."""

RANGE_SPECIFIER = ".."


class ScmStdColumns:
    """SCM Spec File STD Columns."""

    SPEC_ID = "specID"
    NAME = "specName"
    CATEGORY = "category"
    TYPE = "specType"
    UNIT = "unit"
    BLOCK = "block"
    SYMBOL = "specSymbol"
    UPDATED_AT = "lastComplianceUpdatedTimeForSpec"


class ScmGetSpecsResponse:
    """SCM Get Specs Response keys."""

    CONDITIONS = "conditions"
    INFO = "info"
    DATA = "data"
    COLUMN_NAME = "columnName"
    COLUMN_VALUE = "columnValue"
    STATE = "state"
    MESSAGE = "message"


class LimitParams:
    """SLE Specs Limit parameters."""

    MIN = "min"
    MAX = "max"
    TYPICAL = "typical"


class SpecCondParams:
    """SLE Spec Condition Parameters."""

    NAME = "name"
    UNIT = "unit"
    VALUE = "value"
    RANGE = "range"
    DISCRETE = "discrete"


class SleQuerySpecsResponse:
    """SLE QuerySpecs API Response keys."""

    SPECS = "specs"
    PROPERTIES = "properties"
    CONDITION = "conditions"
    LIMIT = "limit"
