"""Test the models."""
from aiohttp import ClientSession
from aresponses import ResponsesMockServer

from odp_gent import BlueBike, Garage, ODPGent, ParkAndRide, Partago

from . import load_fixtures


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
    async with ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[Garage] = await client.garages()
        assert spaces is not None
        for item in spaces:
            assert isinstance(item, Garage)
            assert item.garage_id is not None
            assert item.longitude is not None
            assert item.latitude is not None


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
    async with ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[ParkAndRide] = await client.park_and_rides()
        assert spaces is not None
        for item in spaces:
            assert item.spot_id is not None
            assert item.url is not None
            assert item.availability_pct is not None
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)


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
    async with ClientSession() as session:
        client = ODPGent(session=session)
        spaces: list[ParkAndRide] = await client.park_and_rides(gentse_feesten="True")
        assert spaces is not None
        for item in spaces:
            assert item.spot_id is not None
            assert item.url is not None
            assert item.availability_pct is not None
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)


async def test_bluebikes(aresponses: ResponsesMockServer) -> None:
    """Test bluebikes function."""
    datasets: list[str] = [
        "bluebikes.json",
        "bluebikes.json",
        "bluebikes.json",
        "bluebikes.json",
    ]
    for dataset in datasets:
        aresponses.add(
            "data.stad.gent",
            "/api/records/1.0/search/",
            "GET",
            aresponses.Response(
                status=200,
                headers={"Content-Type": "application/json"},
                text=load_fixtures(dataset),
            ),
        )
    async with ClientSession() as session:
        client = ODPGent(session=session)
        bluebikes: list[BlueBike] = await client.bluebikes()
        assert bluebikes is not None
        for item in bluebikes:
            assert item.spot_id == 72
            assert item.name == "Station Gent-Dampoort"
            assert item.bikes_in_use == 15
            assert item.bikes_available == 45
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)


async def test_partago(aresponses: ResponsesMockServer) -> None:
    """Test partago function."""
    aresponses.add(
        "data.stad.gent",
        "/api/records/1.0/search/",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("partago.json"),
        ),
    )
    async with ClientSession() as session:
        client = ODPGent(session=session)
        partago_vehicles: list[Partago] = await client.partago_vehicles()
        assert partago_vehicles is not None
        for item in partago_vehicles:
            assert item.name is not None
            assert item.picture_url is not None
            assert item.station_type == "free floating"
            assert isinstance(item.longitude, float)
            assert isinstance(item.latitude, float)
