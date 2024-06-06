"""Constants utilized in Error handling of Server end points."""


class ResponseField:
    """Response fields."""

    DATA = "data"
    MESSAGE = "message"
    STATE = "state"


class StatusCode:
    """Status code used when there is error."""

    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500


class ScmResponseStateCodes:
    """SCM Response state codes."""

    SUCCESS = 0
    FAILURE = 1
    ERROR = 2
    NOT_FOUND = 3
