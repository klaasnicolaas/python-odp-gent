"""Basic tests for the Open Data Platform API of Gent."""

# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from odp_gent import ODPGent
from odp_gent.exceptions import ODPGentConnectionError, ODPGentError

from . import load_fixtures


async def test_json_request(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("garages.json"),
        ),
    )
    async with ClientSession() as session:
        client = ODPGent(session=session)
        response = await client._request("test")
        assert response is not None
        await client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test internal session is handled correctly."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("garages.json"),
        ),
    )
    async with ODPGent() as client:
        await client._request("test")


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from the Open Data Platform API of Gent."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!",
            text=load_fixtures("garages.json"),
        )

    aresponses.add("data.stad.gent", "/api/records/1.0/test", "GET", response_handler)

    async with ClientSession() as session:
        client = ODPGent(
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(ODPGentConnectionError):
            assert await client._request("test")


async def test_content_type(aresponses: ResponsesMockServer) -> None:
    """Test request content type error from Open Data Platform API of Gent."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )

    async with ClientSession() as session:
        client = ODPGent(session=session)
        with pytest.raises(ODPGentError):
            assert await client._request("test")


async def test_client_error() -> None:
    """Test request client error from the Open Data Platform API of Gent."""
    async with ClientSession() as session:
        client = ODPGent(session=session)
        with (
            patch.object(
                session,
                "request",
                side_effect=ClientError,
            ),
            pytest.raises(ODPGentConnectionError),
        ):
            assert await client._request("test")
