"""Asynchronous Python client providing Open Data information of Gent."""


class ODPGentError(Exception):
    """Generic Open Data Platform Gent exception."""


class ODPGentConnectionError(ODPGentError):
    """Open Data Platform Gent - connection error."""
