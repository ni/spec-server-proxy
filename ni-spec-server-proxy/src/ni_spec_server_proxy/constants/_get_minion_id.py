"""Constants utilized in Get Minion ID File Path."""

import os
from pathlib import WindowsPath


class MinionIdPath:
    """Paths utilized to get Minion ID."""

    PROGRAM_DATA_PATH = WindowsPath(os.getenv("PROGRAMDATA"))
    MINION_ID_FILE_PATH = PROGRAM_DATA_PATH / "National Instruments" / "salt" / "conf" / "minion_id"
