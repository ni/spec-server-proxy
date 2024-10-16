"""Constants utilized in Get Workspace ID."""

import os
from pathlib import WindowsPath

SYSTEMLINK_WORKSPACE = "systemlink_workspace"


class WorkSpaceIDPath:
    """Paths utilized in get workspace id."""

    program_data_path = os.getenv("PROGRAMDATA")
    if program_data_path:
        PROGRAM_DATA_PATH = WindowsPath(program_data_path)
        SL_CLIENT_GRAIN_FILE_PATH = (
            PROGRAM_DATA_PATH / "National Instruments" / "salt" / "conf" / "grains"
        )
