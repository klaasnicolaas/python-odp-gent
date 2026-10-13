"""Verify full retrieval and original facility identities independently of NIPKaart."""

from copy import deepcopy
from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch

import pytest

from odp_gent import ODPGent, ODPGentError, ParkingFacility


def facility(identity: str = "https://stad.gent/parking/example") -> dict:
    """Return one small source record with a changing portal record ID."""
    return {
        "recordid": "changing-portal-hash",
        "fields": {
            "id": identity,
            "name": "Example",
            "type": "carPark",
            "lastupdate": "2026-10-13T12:03:19+02:00",
            "totalcapacity": 100,
            "availablecapacity": 0,
            "isopennow": 1,
            "temporaryclosed": 0,
        },
        "geometry": {"type": "Point", "coordinates": [3.72, 51.05]},
    }


async def test_complete_pagination(odp_gent_client: ODPGent) -> None:
    """Page using the original ID order and verify every reported record."""
    with patch.object(odp_gent_client, "_request", new_callable=AsyncMock) as request:
        request.side_effect = [
            {"nhits": 3, "records": [facility("a"), facility("b")]},
            {"nhits": 3, "records": [facility("c")]},
        ]
        result = await odp_gent_client.parking_collection(page_size=2)
    assert (result.total_count, result.pages_fetched, result.complete) == (3, 2, True)
    assert [row.facility_id for row in result.records] == ["a", "b", "c"]
    assert request.call_args_list[1].kwargs["params"] == {
        "dataset": "bezetting-parkeergarages-real-time",
        "rows": 2,
        "start": 2,
        "sort": "id",
    }


async def test_empty_collection(odp_gent_client: ODPGent) -> None:
    """A complete empty source is distinct from a failed fetch."""
    with patch.object(
        odp_gent_client, "_request", return_value={"nhits": 0, "records": []}
    ):
        result = await odp_gent_client.parking_collection()
    assert result.complete
    assert result.records == []


@pytest.mark.parametrize(
    "pages",
    [
        [{"nhits": 2, "records": [facility()]}],
        [{"nhits": True, "records": []}],
        [{"nhits": -1, "records": []}],
        [{"nhits": 10001, "records": []}],
        [{"nhits": 1, "records": {}}],
        [{"records": []}],
        [{"nhits": 2, "records": [facility(), facility()]}],
        [
            {"nhits": 3, "records": [facility("a"), facility("b")]},
            {"nhits": 2, "records": []},
        ],
        [
            {"nhits": 3, "records": [facility("a"), facility("b")]},
            {"nhits": 3, "records": []},
        ],
        [{"nhits": 1, "records": [{}]}],
    ],
)
async def test_invalid_collections_fail(odp_gent_client: ODPGent, pages: list) -> None:
    """Never return partial pages, changed totals or duplicated identities."""
    with (
        patch.object(odp_gent_client, "_request", side_effect=pages),
        pytest.raises(ODPGentError),
    ):
        await odp_gent_client.parking_collection(page_size=2)


@pytest.mark.parametrize(
    ("page_size", "max_records"),
    [(0, 1), (101, 1), (True, 1), (1, 0), (1, 10001), (1, True)],
)
async def test_invalid_limits(
    odp_gent_client: ODPGent, page_size: int, max_records: int
) -> None:
    """Safety ceilings cannot be mistaken for complete source retrieval."""
    with pytest.raises(ValueError, match="limits"):
        await odp_gent_client.parking_collection(
            page_size=page_size, max_records=max_records
        )


def test_original_identity_and_measurement() -> None:
    """A refreshed portal hash does not change the facility or date it anew."""
    row = facility()
    parsed = ParkingFacility.from_dict(row)
    row["recordid"] = "new-hash"
    assert ParkingFacility.from_dict(row) == parsed
    assert parsed.facility_id == row["fields"]["id"]
    assert parsed.free_space == 0
    assert parsed.updated_at == datetime(2026, 10, 13, 10, 3, 19, tzinfo=UTC)


@pytest.mark.parametrize("time", [None, "", "bad", "2026-10-13T10:00:00"])
def test_unknown_measurements(time: str | None) -> None:
    """Undated values stay unknown; there is no retrieval-time substitute."""
    row = facility()
    row["fields"].update(
        lastupdate=time,
        totalcapacity=None,
        availablecapacity=None,
        isopennow=None,
        temporaryclosed=None,
    )
    parsed = ParkingFacility.from_dict(row)
    assert parsed.updated_at is None
    assert parsed.free_space is None
    assert parsed.total_capacity is None
    assert parsed.is_open is None
    assert parsed.temporary_closed is None


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("id", None),
        ("id", ""),
        ("name", " "),
        ("type", 1),
        ("totalcapacity", -1),
        ("availablecapacity", True),
        ("availablecapacity", 1.5),
        ("totalcapacity", "1"),
        ("isopennow", "False"),
        ("temporaryclosed", 2),
    ],
)
def test_invalid_source_fields(key: str, value: object) -> None:
    """No invented identity, lossy count or truthy string flag is accepted."""
    row = deepcopy(facility())
    row["fields"][key] = value
    with pytest.raises(ValueError, match="parking"):
        ParkingFacility.from_dict(row)


@pytest.mark.parametrize(
    "geometry",
    [
        {"type": "Polygon", "coordinates": [3.72, 51.05]},
        {"type": "Point", "coordinates": [3.72]},
        {"type": "Point", "coordinates": [True, 51.05]},
        {"type": "Point", "coordinates": [float("nan"), 51.05]},
        {"type": "Point", "coordinates": [181, 51.05]},
        {"type": "Point", "coordinates": [3.72, 91]},
    ],
)
def test_invalid_geometry(geometry: dict) -> None:
    """Provider points must have finite longitude/latitude coordinates."""
    row = facility()
    row["geometry"] = geometry
    with pytest.raises(ValueError, match="parking"):
        ParkingFacility.from_dict(row)
