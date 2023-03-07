# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Gent."""

import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Fetch park and ride using the Gent API client."""
    async with ODPGent() as client:
        park_and_rides = await client.park_and_rides(limit=5, gentse_feesten="True")
        print(park_and_rides)

        count: int
        for index, item in enumerate(park_and_rides, 1):
            count = index
            print(item)
        print("________________________")
        print(f"{count} locations found")


if __name__ == "__main__":
    asyncio.run(main())
