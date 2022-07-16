"""Test the models."""
import aiohttp
import pytest
from aresponses import ResponsesMockServer

from odp_gent import Garage, ODPGent, ParkAndRide

from . import load_fixtures


@pytest.mark.asyncio
async def test_all_garages(aresponses: ResponsesMockServer) -> None:
    """Test all garages function."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/search/",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("garages.json"),
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[Garage] = await client.garages()
        assert spaces is not None
        for item in spaces:
            assert isinstance(item, Garage)
            assert item.garage_id is not None
            assert item.longitude is not None
            assert item.latitude is not None


@pytest.mark.asyncio
async def test_park_and_rides(aresponses: ResponsesMockServer) -> None:
    """Test park and ride spaces function."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/search/",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("park_and_ride.json"),
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[ParkAndRide] = await client.park_and_rides()
        assert spaces is not None
        for item in spaces:
            assert item.spot_id is not None
            assert item.url is not None
            assert item.availability_pct is not None
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)


@pytest.mark.asyncio
async def test_filter_park_and_rides(aresponses: ResponsesMockServer) -> None:
    """Test park and ride spaces filter function."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/search/",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("park_and_ride.json"),
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[ParkAndRide] = await client.park_and_rides(gentse_feesten="True")
        assert spaces is not None
        for item in spaces:
            assert item.spot_id is not None
            assert item.url is not None
            assert item.availability_pct is not None
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)
