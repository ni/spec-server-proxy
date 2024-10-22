"""Constants utilized in Get Minion ID File Path."""

import os
from pathlib import Path


class MinionIdPath:
    """Paths utilized to get Minion ID."""

    program_data_path = os.getenv("PROGRAMDATA")
    if program_data_path:
        PROGRAM_DATA_PATH = Path(program_data_path)
        MINION_ID_FILE_PATH = (
            PROGRAM_DATA_PATH / "National Instruments" / "salt" / "conf" / "minion_id"
        )
