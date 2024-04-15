"""Fixtures for the ODP Gent tests."""

from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from odp_gent import ODPGent


@pytest.fixture(name="odp_gent_client")
async def client() -> AsyncGenerator[ODPGent, None]:
    """ODP Gent client fixture."""
    async with (
        ClientSession() as session,
        ODPGent(session=session) as odp_gent_client,
    ):
        yield odp_gent_client
