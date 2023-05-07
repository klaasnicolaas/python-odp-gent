"""Asynchronous Python client providing Open Data information of Gent."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, cast

import async_timeout
from aiohttp import ClientError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import ODPGentConnectionError, ODPGentError
from .models import BlueBike, Garage, ParkAndRide, Partago


@dataclass
class ODPGent:
    """Main class for handling data fetchting from Open Data Platform of Gent."""

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Open Data Platform API of Gent.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'
            method: HTTP method to use, for example, 'GET'
            params: Extra options to improve or limit the response.

        Returns:
        -------
            A Python dictionary (text) with the response from
            the Open Data Platform API of Gent.

        Raises:
        ------
            ODPGentConnectionError: Timeout occurred while
                connecting to the Open Data Platform API.
            ODPGentError: If the data is not valid.
        """
        version = metadata.version(__package__)
        url = URL.build(
            scheme="https",
            host="data.stad.gent",
            path="/api/records/1.0/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonODPGent/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    params=params,
                    headers=headers,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the Open Data Platform API."
            raise ODPGentConnectionError(msg) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with Open Data Platform API."
            raise ODPGentConnectionError(msg) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the Open Data Platform API"
            raise ODPGentError(
                msg,
                {"Content-Type": content_type, "Response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def garages(self, limit: int = 10) -> list[Garage]:
        """Get list of parking garages.

        Args:
        ----
            limit: Maximum number of garages to return.

        Returns:
        -------
            A list of Garage objects.
        """
        results: list[Garage] = []
        locations = await self._request(
            "search/",
            params={"dataset": "bezetting-parkeergarages-real-time", "rows": limit},
        )

        for item in locations["records"]:
            results.append(Garage.from_dict(item))
        return results

    async def park_and_rides(
        self,
        limit: int = 10,
        gentse_feesten: str | None = None,
    ) -> list[ParkAndRide]:
        """Get list of Park and Ride locations.

        Args:
        ----
            limit: Maximum number of garages to return.
            gentse_feesten: Filter by Gentse Feesten.

        Returns:
        -------
            A list of ParkAndRide objects.
        """
        results: list[ParkAndRide] = []
        params: dict[str, Any] = {
            "dataset": "real-time-bezetting-pr-gent",
            "rows": limit,
        }

        if gentse_feesten is not None:
            params["refine.gentse_feesten"] = gentse_feesten

        locations = await self._request(
            "search/",
            params=params,
        )

        for item in locations["records"]:
            results.append(ParkAndRide.from_dict(item))
        return results

    async def bluebikes(self) -> list[BlueBike]:
        """Get list of data from BlueBike locations.

        Returns
        -------
            A list of BlueBike objects.
        """
        results: list[BlueBike] = []

        # Data is spread over multiple datasets
        datasets: list[str] = [
            "blue-bike-deelfietsen-gent-sint-pieters-st-denijslaan",
            "blue-bike-deelfietsen-merelbeke-drongen-wondelgem",
            "blue-bike-deelfietsen-gent-sint-pieters-m-hendrikaplein",
            "blue-bike-deelfietsen-gent-dampoort",
        ]

        for dataset in datasets:
            locations = await self._request(
                "search/",
                params={"dataset": dataset},
            )

            for item in locations["records"]:
                results.append(BlueBike.from_dict(item))
        return results

    async def partago_vehicles(self, limit: int = 10) -> list[Partago]:
        """Get list of data from Partago vehicles.

        Returns
        -------
            A list of Partago objects.
        """
        results: list[Partago] = []
        vehicles = await self._request(
            "search/",
            params={"dataset": "real-time-locaties-deelwagen-partago", "rows": limit},
        )

        for item in vehicles["records"]:
            results.append(Partago.from_dict(item))
        return results

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> ODPGent:
        """Async enter.

        Returns
        -------
            The Open Data Platform Gent object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
