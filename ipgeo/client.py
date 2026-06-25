"""IPGeo API client."""

from typing import Any, Optional

import requests


class IPGeoClient:
    """IP geolocation API client with built-in security detection.

    Usage:
        >>> client = IPGeoClient("ipgeo_YOUR_API_KEY")
        >>> data = client.lookup("8.8.8.8")
        >>> print(data["location"]["country"]["name"])
        United States
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.getipgeo.com",
        timeout: int = 10,
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({
            "X-API-Key": api_key,
            "Accept": "application/json",
            "User-Agent": f"ipgeo-python/{__import__('ipgeo').__version__}",
        })

    # -- IP Lookup ----------------------------------------------------------

    def lookup(self, ip: str, fields: Optional[str] = None) -> dict[str, Any]:
        """Look up geolocation for an IP address.

        Args:
            ip: IPv4 or IPv6 address, or 'me' for the caller's own IP.
            fields: Comma-separated field groups (e.g. 'location,security').

        Returns:
            Dict with ip, location, network, security, meta keys.
        """
        params = {"fields": fields} if fields else {}
        resp = self._session.get(
            f"{self._base_url}/v1/ip/{ip}",
            params=params,
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return resp.json()

    def me(self) -> dict[str, Any]:
        """Look up the calling client's own IP address."""
        return self.lookup("me")

    # -- Batch --------------------------------------------------------------

    def batch(self, ips: list[str]) -> dict[str, Any]:
        """Look up up to 100 IP addresses in a single request.

        Args:
            ips: List of IPv4 or IPv6 addresses (max 100).

        Returns:
            Dict with 'results' key containing a list of lookup results.
        """
        resp = self._session.post(
            f"{self._base_url}/v1/ip/batch",
            json={"ips": ips},
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return resp.json()

    # -- Usage --------------------------------------------------------------

    def usage(self) -> dict[str, Any]:
        """Get current billing period usage.

        Returns:
            Dict with plan, monthly_quota, monthly_used, remaining_quota, prepaid_credits.
        """
        resp = self._session.get(
            f"{self._base_url}/v1/usage",
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return resp.json()

    # -- Health -------------------------------------------------------------

    def health(self) -> dict[str, Any]:
        """Check API health status. No authentication required."""
        resp = self._session.get(
            f"{self._base_url}/v1/health",
            timeout=self._timeout,
        )
        resp.raise_for_status()
        return resp.json()
