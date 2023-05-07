# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Gent."""

import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Fetch Partago data using the Gent API client."""
    async with ODPGent() as client:
        partago_vehicles = await client.partago_vehicles(limit=120)

        count: int
        for index, item in enumerate(partago_vehicles, 1):
            count = index
            print(item)
        print("________________________")
        print(f"{count} partago cars found")


if __name__ == "__main__":
    asyncio.run(main())
