"""Models for Open Data Platform of Gent."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from math import isfinite
from typing import Any

import pytz


@dataclass
class Garage:
    """Object representing a garage."""

    garage_id: str
    name: str
    parking_type: str
    url: str

    is_open: bool
    free_parking: bool
    temporary_closed: bool

    free_space: int
    total_capacity: int
    availability_pct: float
    occupation_pct: int

    longitude: float
    latitude: float
    updated_at: datetime

    @classmethod
    def from_dict(cls: type[Garage], data: dict[str, Any]) -> Garage:
        """Return a Garage object from a dictionary.

        Args:
        ----
            data: The data from the API.

        Returns:
        -------
            A Garage object.

        """
        attr = data["fields"]
        geo = data["geometry"]["coordinates"]
        return cls(
            garage_id=str(data.get("recordid")),
            name=attr.get("name"),
            parking_type=attr.get("type"),
            url=attr.get("urllinkaddress"),
            is_open=bool(attr.get("isopennow")),
            free_parking=bool(attr.get("freeparking")),
            temporary_closed=bool(attr.get("temporaryclosed")),
            free_space=attr.get("availablecapacity"),
            total_capacity=attr.get("totalcapacity"),
            availability_pct=round(
                (
                    float(attr.get("availablecapacity"))
                    / float(attr.get("totalcapacity"))
                )
                * 100,
                1,
            ),
            occupation_pct=attr.get("occupation"),
            longitude=geo[0],
            latitude=geo[1],
            updated_at=datetime.strptime(attr.get("lastupdate"), "%Y-%m-%dT%H:%M:%S%z"),
        )


@dataclass
class ParkAndRide:
    """Object representing a park and ride spot."""

    spot_id: str
    name: str
    parking_type: str
    url: str

    is_open: bool
    free_parking: bool
    temporary_closed: bool
    gentse_feesten: bool

    free_space: int
    total_capacity: int
    availability_pct: float
    occupation_pct: int

    longitude: float
    latitude: float
    updated_at: datetime

    @classmethod
    def from_dict(cls: type[ParkAndRide], data: dict[str, Any]) -> ParkAndRide:
        """Return a ParkAndRide object from a dictionary.

        Args:
        ----
            data: The data from the API.

        Returns:
        -------
            A ParkAndRide object.

        """
        attr = data["fields"]
        geo = data["geometry"]["coordinates"]
        return cls(
            spot_id=str(data.get("recordid")),
            name=attr.get("name"),
            parking_type=attr.get("type"),
            url=attr.get("urllinkaddress"),
            is_open=bool(attr.get("isopennow")),
            free_parking=bool(attr.get("freeparking")),
            temporary_closed=bool(attr.get("temporaryclosed")),
            gentse_feesten=bool(attr.get("gentse_feesten") == "True"),
            free_space=attr.get("availablespaces"),
            total_capacity=attr.get("numberofspaces"),
            availability_pct=round(
                (float(attr.get("availablespaces")) / float(attr.get("numberofspaces")))
                * 100,
                1,
            ),
            occupation_pct=attr.get("occupation"),
            longitude=geo[0],
            latitude=geo[1],
            updated_at=datetime.strptime(attr.get("lastupdate"), "%Y-%m-%dT%H:%M:%S%z"),
        )


@dataclass
class BlueBike:
    """Object representing a BlueBike rental location."""

    spot_id: str
    name: str
    spot_type: int

    bikes_in_use: int
    bikes_available: int
    last_update: datetime

    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls: type[BlueBike], data: dict[str, Any]) -> BlueBike:
        """Return a BlueBike object from a dictionary.

        Args:
        ----
            data: The data from the API.

        Returns:
        -------
            A BlueBike object.

        """
        attr = data["fields"]
        return cls(
            spot_id=attr.get("id"),
            name=attr.get("name"),
            spot_type=int(attr.get("type")),
            bikes_in_use=attr.get("bikes_in_use"),
            bikes_available=attr.get("bikes_available"),
            last_update=datetime.strptime(
                attr.get("last_seen"),
                "%Y-%m-%dT%H:%M:%S%z",
            ).replace(tzinfo=pytz.timezone("Europe/Brussels")),
            longitude=float(attr.get("longitude")),
            latitude=float(attr.get("latitude")),
        )


@dataclass
class Partago:
    """Object representing a Partago vehicle location."""

    name: str
    vehicle_type: Vehicle
    picture_url: str | None
    station_type: str
    last_update: datetime

    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls: type[Partago], data: dict[str, Any]) -> Partago:
        """Return a Partago vehicle object from a dictionary.

        Args:
        ----
            data: The data from the API.

        Returns:
        -------
            A Partago object.

        """
        attr = data["fields"]
        geo = data["geometry"]["coordinates"]
        return cls(
            name=attr.get("displayname"),
            vehicle_type=Vehicle.from_dict(json.loads(attr.get("vehicleinformation"))),
            picture_url=None if attr.get("picture") == "null" else attr.get("picture"),
            station_type=attr.get("stationtype"),
            last_update=datetime.strptime(
                data["record_timestamp"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ).replace(tzinfo=pytz.utc),
            longitude=geo[0],
            latitude=geo[1],
        )


@dataclass
class Vehicle:
    """Object representing a general vehicle."""

    brand: str
    mode: str
    fuel_type: str
    transmission_type: str

    @classmethod
    def from_dict(cls: type[Vehicle], data: dict[str, Any]) -> Vehicle:
        """Return a Vehicle object from a dictionary.

        Args:
        ----
            data: The data from the API.


        Returns:
        -------
            A Vehicle object.

        """
        return cls(
            brand=data["brand"],
            mode=data["model"],
            fuel_type=data["fuelType"],
            transmission_type=data["transmissionType"],
        )


@dataclass(frozen=True)
class ParkingFacility:
    """Original facility identity and nullable measurements from the live feed.

    Unlike a portal recordid, fields.id identifies the facility independently
    of occupancy refreshes. Counts cover general parking, not accessible bays.
    """

    facility_id: str
    name: str
    parking_type: str
    longitude: float
    latitude: float
    updated_at: datetime | None
    total_capacity: int | None
    free_space: int | None
    is_open: bool | None
    temporary_closed: bool | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ParkingFacility:
        """Parse source claims without substituting retrieval time or zero."""
        fields = data["fields"]
        identity, name, parking_type = (
            fields.get(key) for key in ("id", "name", "type")
        )
        if any(
            not isinstance(value, str) or not value.strip()
            for value in (identity, name, parking_type)
        ):
            msg = "Missing parking facility identity, name or type"
            raise ValueError(msg)
        geometry = data["geometry"]
        coordinates = geometry["coordinates"]
        if (
            geometry["type"] != "Point"
            or len(coordinates) != 2
            or any(
                type(value) not in (float, int) or not isfinite(value)
                for value in coordinates
            )
            or not -180 <= coordinates[0] <= 180
            or not -90 <= coordinates[1] <= 90
        ):
            msg = "Invalid parking facility coordinates"
            raise ValueError(msg)
        measured_at = None
        if fields.get("lastupdate"):
            try:
                measured_at = datetime.fromisoformat(fields["lastupdate"])
            except ValueError:
                measured_at = None
            if measured_at is not None and measured_at.utcoffset() is None:
                measured_at = None
        return cls(
            facility_id=identity,
            name=name,
            parking_type=parking_type,
            longitude=coordinates[0],
            latitude=coordinates[1],
            updated_at=measured_at,
            total_capacity=_parking_count(fields.get("totalcapacity")),
            free_space=_parking_count(fields.get("availablecapacity")),
            is_open=_parking_flag(fields.get("isopennow")),
            temporary_closed=_parking_flag(fields.get("temporaryclosed")),
        )


def _parking_count(value: object) -> int | None:
    """Reject lossy, negative and boolean capacity values."""
    if value is None:
        return None
    if type(value) is not int or value < 0:
        msg = "Invalid parking count"
        raise ValueError(msg)
    return value


def _parking_flag(value: object) -> bool | None:
    """Keep missing source health/open flags unknown."""
    if value is None:
        return None
    if type(value) not in (int, bool) or value not in (0, 1):
        msg = "Invalid parking flag"
        raise ValueError(msg)
    return bool(value)
