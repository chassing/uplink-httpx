import asyncio
import logging
from functools import wraps

from uplink.clients import exceptions, interfaces, io

try:
    import httpx
except ImportError:
    httpx = None

log = logging.getLogger("uplink.httpx")
ssl_context = httpx.create_ssl_context()


def threaded_callback(callback):
    @wraps(callback)
    async def new_callback(*args, **kwargs):
        return callback(*args, **kwargs)

    return new_callback


class HttpxClient(interfaces.HttpClientAdapter):
    exceptions = exceptions.Exceptions()

    def __init__(self, session=None, verify=True, **kwargs):
        if httpx is None:
            raise NotImplementedError("httpx is not installed.")
        self._session = session or httpx.AsyncClient(verify=ssl_context if verify else False, **kwargs)
        self._sync_callback_adapter = threaded_callback

    def __del__(self):
        log.debug("HttpxClient: __del__")
        try:
            if not self._session.is_closed:
                asyncio.create_task(self._session.aclose())
        except RuntimeError:
            pass

    async def __aenter__(self):
        log.debug("HttpxClient: __aenter__")
        await self._session.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        log.debug("HttpxClient: __aexit__")
        await self._session.__aexit__()

    async def send(self, request):
        method, url, extras = request
        response = await self._session.request(method=method, url=url, **extras)
        return response

    def wrap_callback(self, callback):
        if not asyncio.iscoroutinefunction(callback):
            callback = self._sync_callback_adapter(callback)
        return callback

    def apply_callback(self, callback, response):
        return self.wrap_callback(callback)(response)

    @staticmethod
    def io():
        return io.AsyncioStrategy()


HttpxClient.exceptions.BaseClientException = httpx.HTTPStatusError
HttpxClient.exceptions.ConnectionError = httpx.RequestError
HttpxClient.exceptions.ConnectionTimeout = httpx.TimeoutException
HttpxClient.exceptions.ServerTimeout = httpx.TimeoutException
HttpxClient.exceptions.SSLError = httpx.RequestError
HttpxClient.exceptions.InvalidURL = httpx.InvalidURL
