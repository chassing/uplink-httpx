[![code formatting][black_badge]][black_base]
[![pypi badge][pypi_badge]][pypi_base]
![](https://github.com/chassing/uplink-httpx/workflows/Test/badge.svg)

# uplink-httpx

Uplink-Httpx is an asynchronous HTTP client based on [HTTPX](https://www.encode.io/httpx/) for the awesome [Uplink](https://uplink.readthedocs.io/en/stable/) REST library.

Use it like any other HTTP client for uplink.

```python
import asyncio

import uplink

from uplink_httpx import HttpxClient


@uplink.headers({"Accept": "application/json"})
@uplink.returns.json()
class HttpBin(uplink.Consumer):
    @uplink.get("get")
    def get(self):
        pass


async def demo():
    httpbin = HttpBin(base_url="https://httpbin.org", client=HttpxClient())
    resp = await httpbin.get()
    print(resp)
    # {'args': {}, 'headers': {'Accept': 'application/json', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-httpx/0.9.5'}, ... 'url': 'https://httpbin.org/get'}


loop = asyncio.get_event_loop()
loop.run_until_complete(demo())

```

## Features

[HTTPX](https://www.encode.io/httpx/) builds on the well-established usability of `requests`, and gives you:

* A requests-compatible API wherever possible. No [issues](https://github.com/prkumar/uplink/issues/174) between async and sync clients anymore.
* HTTP/2 and HTTP/1.1 support.
* Strict timeouts everywhere.



[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_base]: https://github.com/ambv/black
[pypi_badge]: https://img.shields.io/pypi/v/uplink-httpx.svg
[pypi_base]: https://pypi.python.org/pypi/uplink-httpx
