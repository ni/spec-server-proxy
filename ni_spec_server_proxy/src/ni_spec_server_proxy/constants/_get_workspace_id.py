"""Constants utilized in Get Workspace ID."""

import os
from pathlib import WindowsPath

SYSTEMLINK_WORKSPACE = "systemlink_workspace"


class WorkSpaceIDPath:
    """Paths utilized in get workspace id."""

    PROGRAM_DATA_PATH = WindowsPath(os.getenv("PROGRAMDATA"))
    SL_CLIENT_GRAIN_FILE_PATH = (
        PROGRAM_DATA_PATH / "National Instruments" / "salt" / "conf" / "grains"
    )
