<!-- Banner -->
![alt Banner of the odp gent package](https://raw.githubusercontent.com/klaasnicolaas/python-odp-gent/main/assets/header_odp_gent-min.png)

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![PyPi Downloads][downloads-shield]][downloads-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

[![Code Quality][code-quality-shield]][code-quality]
[![Build Status][build-shield]][build-url]
[![Typing Status][typing-shield]][typing-url]

[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]

Asynchronous Python client for the open datasets of Gent (Belgium).

## About

A python package with which you can retrieve data from the Open Data Platform of Gent via [their API][api]. This package was initially created to only retrieve parking data from the API, but the code base is made in such a way that it is easy to extend for other datasets from the same platform.

## Installation

```bash
pip install odp-gent
```

## Datasets

You can read the following datasets with this package:

- Parking garages occupancy (12 locations)
- Park and Ride occupancy (5 locations)

<details>
    <summary>Click here to get more details</summary>

### Parking garages

Parameters:

- **limit** (default: 10) - How many results you want to retrieve.

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `garage_id` | string | The id of the garage |
| `name` | string | The name of the garage |
| `parking_type` | string | The type of parking |
| `url` | string | The url with more information about the garage |
| `is_open` | boolean | Whether the garage is open or not |
| `free_parking` | boolean | Whether there is free parking or not |
| `temporary_closed` | boolean | Whether the garage is temporarily closed or not |
| `free_space` | integer | The amount of free parking spaces |
| `total_capacity` | integer | The total capacity of the garage |
| `availability_pct` | float | The percentage of free parking spaces |
| `occupancy_pct` | integer | The percentage of occupied parking spaces |
| `longitude` | float | The longitude of the garage |
| `latitude` | float | The latitude of the garage |
| `updated_at` | datetime | The last time the data was updated |

### Park and Ride

Parameters:

- **limit** (default: 10) - How many results you want to retrieve.
- **gentse_feesten** - Whether a park and ride location is used for the [Gentse Feesten](https://gentsefeesten.stad.gent).

| Variable | Type | Description |
| :------- | :--- | :---------- |
| `spot_id` | string | The id of the park and ride |
| `name` | string | The name of the park and ride |
| `parking_type` | string | The type of parking |
| `url` | string | The url with more information about the park and ride |
| `is_open` | boolean | Whether the park and ride is open or not |
| `free_parking` | boolean | Whether there is free parking or not |
| `temporary_closed` | boolean | Whether the park and ride is temporarily closed or not |
| `gentse_feesten` | boolean | Whether the park and ride is used for the [Gentse Feesten](https://gentsefeesten.stad.gent) |
| `free_space` | integer | The amount of free parking spaces |
| `total_capacity` | integer | The total capacity of the park and ride |
| `availability_pct` | float | The percentage of free parking spaces |
| `occupancy_pct` | integer | The percentage of occupied parking spaces |
| `longitude` | float | The longitude of the park and ride |
| `latitude` | float | The latitude of the park and ride |
| `updated_at` | datetime | The last time the data was updated |
</details>

## Example

```python
import asyncio

from odp_gent import ODPGent


async def main() -> None:
    """Show example on using the Open Data API client."""
    async with ODPGent() as client:
        garages = await client.garages(limit=12)
        park_and_rides = await client.park_and_rides(limit=5, gentse_feesten="True")
        print(garages)
        print(park_and_rides)


if __name__ == "__main__":
    asyncio.run(main())
```

## Use cases

[NIPKaart.nl][nipkaart]

A website that provides insight into where disabled parking spaces are, based
on data from users and municipalities. Operates mainly in the Netherlands, but
also has plans to process data from abroad.

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.9+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## License

MIT License

Copyright (c) 2022-2023 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[api]: https://data.stad.gent/explore
[nipkaart]: https://www.nipkaart.nl

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/tests.yaml
[code-quality-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/codeql.yaml/badge.svg
[code-quality]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/codeql.yaml
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-odp-gent.svg
[commits-url]: https://github.com/klaasnicolaas/python-odp-gent/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-odp-gent/branch/main/graph/badge.svg?token=5JNbz4akUL
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-odp-gent
[downloads-shield]: https://img.shields.io/pypi/dm/odp-gent
[downloads-url]: https://pypistats.org/packages/odp-gent
[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-odp-gent.svg
[issues-url]: https://github.com/klaasnicolaas/python-odp-gent/issues
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-odp-gent.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-odp-gent.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2023.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/ceb27fb15cf0e485dc23/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-odp-gent/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[pypi]: https://pypi.org/project/odp-gent/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/odp-gent
[typing-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/typing.yaml
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-odp-gent.svg
[releases]: https://github.com/klaasnicolaas/python-odp-gent/releases
[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-odp-gent.svg
[stars-url]: https://github.com/klaasnicolaas/python-odp-gent/stargazers

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
