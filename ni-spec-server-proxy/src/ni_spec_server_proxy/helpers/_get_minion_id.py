"""Retrieve Minion ID from SystemLink Client `minion_id` file."""

from ni_spec_server_proxy.constants import MinionIdPath


def get_minion_id() -> str:
    """Get Minion ID of the connected remote system.

    Read Minion ID from `minion_id` file of SystemLink Client.

    Returns:
        str: Minion ID of the system.
    """
    minion_id = None

    with open(MinionIdPath.MINION_ID_FILE_PATH, "r") as f:
        minion_id = f.read()

    return minion_id
