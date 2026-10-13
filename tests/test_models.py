"""Test the models."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from odp_gent import BlueBike, Partago

from . import load_fixtures

if TYPE_CHECKING:
    from odp_gent import Garage, ODPGent, ParkAndRide


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


@pytest.mark.parametrize(
    ("source_time", "expected"),
    [
        ("2023-05-06T20:34:59+00:00", datetime(2023, 5, 6, 20, 34, 59, tzinfo=UTC)),
        ("2026-07-01T12:00:00+02:00", datetime(2026, 7, 1, 10, tzinfo=UTC)),
        ("2026-01-01T12:00:00+01:00", datetime(2026, 1, 1, 11, tzinfo=UTC)),
    ],
)
def test_bluebike_preserves_source_offset(source_time: str, expected: datetime) -> None:
    """Do not overwrite a dated source offset with a Brussels timezone label."""
    record = json.loads(load_fixtures("bluebikes.json"))["records"][0]
    record["fields"]["last_seen"] = source_time

    measured_at = BlueBike.from_dict(record).last_update

    assert measured_at == expected
    assert measured_at.isoformat() == source_time


@pytest.mark.parametrize(
    ("source_time", "microseconds"),
    [("2023-05-07T12:00:08.601Z", 601000), ("2023-05-07T12:00:08Z", 0)],
)
def test_partago_preserves_utc_and_fractional_seconds(
    source_time: str, microseconds: int
) -> None:
    """The Z suffix already identifies UTC; do not attach a third-party timezone."""
    record = json.loads(load_fixtures("partago.json"))["records"][0]
    record["record_timestamp"] = source_time

    measured_at = Partago.from_dict(record).last_update

    assert measured_at.utcoffset() == timedelta(0)
    assert measured_at.tzinfo == UTC
    assert measured_at == datetime(2023, 5, 7, 12, 0, 8, microseconds, tzinfo=UTC)


@pytest.mark.parametrize(
    ("fixture", "model", "field"),
    [
        ("bluebikes.json", BlueBike, "last_seen"),
        ("partago.json", Partago, "record_timestamp"),
    ],
)
def test_source_times_without_an_offset_are_rejected(
    fixture: str, model: type[BlueBike | Partago], field: str
) -> None:
    """Removing pytz must not make timezone-free source times acceptable."""
    record = json.loads(load_fixtures(fixture))["records"][0]
    target = record["fields"] if field == "last_seen" else record
    target[field] = "2026-10-13T12:00:00"

    with pytest.raises(ValueError, match="timezone"):
        model.from_dict(record)
