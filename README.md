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
[![Open in Dev Containers][devcontainer-shield]][devcontainer]

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

- [Parking garages occupancy][garages] (12 locations)
- [Park and Ride occupancy][parkandride] (5 locations)
- [BlueBike rental locations][bluebike] (6 locations)
- [Partago vehicle locations][partago] (116 locations)

Find here [more information](examples) about the different variables and parameters per dataset with this python package.

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
You can find more code examples in the [examples](examples) folder.

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

The simplest way to begin is by utilizing the [Dev Container][devcontainer]
feature of Visual Studio Code or by opening a CodeSpace directly on GitHub.
By clicking the button below you immediately start a Dev Container in Visual Studio Code.

[![Open in Dev Containers][devcontainer-shield]][devcontainer]

This Python project relies on [Poetry][poetry] as its dependency manager,
providing comprehensive management and control over project dependencies.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]

### Installation

Install all packages, including all development requirements:

```bash
poetry install
```

_Poetry creates by default an virtual environment where it installs all
necessary pip packages_.

### Pre-commit

This repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. To setup the pre-commit check, run:

```bash
poetry run pre-commit install
```

And to run all checks and tests manually, use the following command:

```bash
poetry run pre-commit run --all-files
```

### Testing

It uses [pytest](https://docs.pytest.org/en/stable/) as the test framework. To run the tests:

```bash
poetry run pytest
```

To update the [syrupy](https://github.com/tophat/syrupy) snapshot tests:

```bash
poetry run pytest --snapshot-update
```

## License

MIT License

Copyright (c) 2022-2025 Klaas Schoute

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

[garages]: https://data.stad.gent/explore/dataset/bezetting-parkeergarages-real-time/information
[parkandride]: https://data.stad.gent/explore/dataset/real-time-bezetting-pr-gent/information
[bluebike]: https://data.stad.gent/explore/?disjunctive.keyword&disjunctive.theme&sort=modified&q=bluebike
[partago]: https://data.stad.gent/explore/dataset/real-time-locaties-deelwagen-partago/information

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/tests.yaml
[code-quality-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/codeql.yaml/badge.svg
[code-quality]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/codeql.yaml
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-odp-gent.svg
[commits-url]: https://github.com/klaasnicolaas/python-odp-gent/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-odp-gent/branch/main/graph/badge.svg?token=5JNbz4akUL
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-odp-gent
[devcontainer-shield]: https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/klaasnicolaas/python-odp-gent
[downloads-shield]: https://img.shields.io/pypi/dm/odp-gent
[downloads-url]: https://pypistats.org/packages/odp-gent
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-odp-gent.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-odp-gent.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/ceb27fb15cf0e485dc23/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-odp-gent/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[pypi]: https://pypi.org/project/odp-gent/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/odp-gent
[typing-shield]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/klaasnicolaas/python-odp-gent/actions/workflows/typing.yaml
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-odp-gent.svg
[releases]: https://github.com/klaasnicolaas/python-odp-gent/releases

[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
