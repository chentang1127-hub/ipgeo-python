# IPGeo Python SDK

[![PyPI](https://img.shields.io/badge/pypi-ipgeo-blue)](https://pypi.org/project/ipgeo-api/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

Free IP geolocation API client with built-in security detection — VPN, proxy, Tor, and hosting flags included on every plan. Zero infrastructure, one API key.

## Install

```bash
pip install ipgeo-api
```

## Quick Start

```python
from ipgeo import IPGeoClient

client = IPGeoClient("ipgeo_YOUR_API_KEY")

# Look up an IP
data = client.lookup("8.8.8.8")
print(data["location"]["country"]["name"])  # United States
print(data["security"]["is_hosting"])       # True

# Look up your own IP
me = client.me()
print(me["ip"])

# Batch lookup (up to 100 IPs)
result = client.batch(["8.8.8.8", "1.1.1.1", "8.8.4.4"])
for r in result["results"]:
    print(r["ip"], r["location"]["country"]["code"])

# Field filtering — only get what you need
data = client.lookup("8.8.8.8", fields="country,security")
# Returns only location (country needed) + security blocks

# Check usage
usage = client.usage()
print(f"{usage['remaining_quota']}/{usage['monthly_quota']} remaining")
```

## Response Structure

```json
{
  "ip": "8.8.8.8",
  "location": {
    "country": {"code": "US", "name": "United States"},
    "city": "Mountain View",
    "latitude": 37.4223,
    "longitude": -122.0842,
    "timezone": "America/Los_Angeles"
  },
  "network": {
    "isp": "Google LLC",
    "asn": 15169,
    "type": "hosting"
  },
  "security": {
    "is_tor": false,
    "is_vpn": false,
    "is_proxy": false,
    "is_hosting": true
  },
  "meta": {
    "data_source": "GeoLite2"
  }
}
```

## API Reference

### `IPGeoClient(api_key, base_url?, timeout?)`

| Param | Default | Description |
|-------|---------|-------------|
| `api_key` | (required) | Your IPGeo API key |
| `base_url` | `https://api.getipgeo.com` | API server URL |
| `timeout` | `10` | Request timeout in seconds |

### Methods

| Method | Description |
|--------|-------------|
| `lookup(ip, fields?)` | Look up a single IP address |
| `me()` | Look up the caller's own IP |
| `batch(ips)` | Look up up to 100 IPs at once |
| `usage()` | Check monthly quota usage |
| `health()` | API health check (no auth) |

## Plans

| Plan | Monthly Quota | Rate Limit |
|------|---------------|------------|
| Free | 10,000 | 60/min |
| Starter | 100,000 | 600/min |
| Pro | 500,000 | 3,000/min |
| Business | 1,000,000 | 10,000/min |

[See all plans →](https://getipgeo.com/pricing)

## License

MIT · [IPGeo](https://getipgeo.com)
