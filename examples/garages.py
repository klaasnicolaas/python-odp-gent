# pylint: disable=W0621
"""Asynchronous Python client providing Open Data information of Gent."""

import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Fetch garages using the Gent API client."""
    async with ODPGent() as client:
        garages = await client.garages(limit=12)
        print(garages)

        count: int = len(garages)
        for item in garages:
            print(item)

        print("______________________")
        print(f"{count} garages found")


if __name__ == "__main__":
    asyncio.run(main())
