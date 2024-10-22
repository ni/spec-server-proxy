"""Retrieve Workspace ID from `SystemLink Client Grain File`."""

from typing import Dict

import yaml

from ni_spec_server_proxy.constants import SYSTEMLINK_WORKSPACE, WorkSpaceIDPath


def get_system_workspace() -> str:
    """Get the workspace of the connected remote system.

    Read workspace from `grains` file of SystemLink Client.

    Returns:
        str: Workspace Id of the system.
    """
    with open(WorkSpaceIDPath.SL_CLIENT_GRAIN_FILE_PATH, "r") as fp:
        grain_data: Dict = yaml.safe_load(fp)

    return str(grain_data.get(SYSTEMLINK_WORKSPACE))
