"""Pytest configuration file."""

import asyncio
import io
import os
from typing import Callable, Dict, Generator

import pytest
from flask.testing import FlaskClient
from werkzeug.datastructures import FileStorage

from ni_spec_server_proxy.main import app

# Set event loop policy to avoid RuntimeError.
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """Fixture that creates a Flask test client."""
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def get_upload_measurement_data() -> Generator[Callable[[str], Dict[str, FileStorage]], None, None]:
    """Fixture to return upload measurement data."""

    def _get_upload_measurement_data(file_path: str) -> Dict[str, FileStorage]:
        with open(file_path, "rb") as f:
            file_content = f.read()

        data = {
            "formCollection": (
                FileStorage(
                    stream=io.BytesIO(file_content),
                    filename=os.path.basename(file_path),
                    content_type="text/csv",
                )
            )
        }

        return data

    yield _get_upload_measurement_data
