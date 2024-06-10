"""Pytest configuration file."""

import pytest

from ni_spec_server_proxy.main import app


@pytest.fixture(scope="function")
def client():
    """Test fixture that creates a Flaks test client."""
    with app.test_client() as test_client:
        yield test_client
