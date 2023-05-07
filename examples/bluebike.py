# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Gent."""

import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Fetch bluebike data using the Gent API client."""
    async with ODPGent() as client:
        bluebiks = await client.bluebikes()

        count: int
        for index, item in enumerate(bluebiks, 1):
            count = index
            print(item)
        print("__________________________")
        print(f"{count} bluebike locations found")


if __name__ == "__main__":
    asyncio.run(main())
