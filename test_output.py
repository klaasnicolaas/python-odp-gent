# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Gent."""

import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Show example on using the Gent API client."""
    async with ODPGent() as client:
        garages = await client.garages(limit=12)
        park_and_rides = await client.park_and_rides(limit=5)
        # print(park_and_rides)

        index: int
        for index, item in enumerate(garages, 1):
            print(item)
        print(f"{index} locations found")


if __name__ == "__main__":
    asyncio.run(main())
