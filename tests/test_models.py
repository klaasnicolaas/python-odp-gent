"""Test the models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from . import load_fixtures

if TYPE_CHECKING:
    from odp_gent import BlueBike, Garage, ODPGent, ParkAndRide, Partago


async def test_all_garages(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_gent_client: ODPGent,
) -> None:
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
    spaces: list[Garage] = await odp_gent_client.garages()
    assert spaces == snapshot


async def test_park_and_rides(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_gent_client: ODPGent,
) -> None:
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
    spaces: list[ParkAndRide] = await odp_gent_client.park_and_rides()
    assert spaces == snapshot


async def test_filter_park_and_rides(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_gent_client: ODPGent,
) -> None:
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
    spaces: list[ParkAndRide] = await odp_gent_client.park_and_rides(
        gentse_feesten="True"
    )
    assert spaces == snapshot


async def test_bluebikes(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_gent_client: ODPGent,
) -> None:
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
    bluebikes: list[BlueBike] = await odp_gent_client.bluebikes()
    assert bluebikes == snapshot


async def test_partago(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    odp_gent_client: ODPGent,
) -> None:
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
    partago_vehicles: list[Partago] = await odp_gent_client.partago_vehicles()
    assert partago_vehicles == snapshot
