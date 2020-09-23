import asyncio
import logging

from uplink.clients import exceptions, interfaces, io, register

try:
    import httpx
except ImportError:
    httpx = None


log = logging.getLogger("uplink.httpx")


def threaded_callback(callback):
    coroutine_callback = asyncio.coroutine(callback)

    @asyncio.coroutine
    def new_callback(response):
        response = yield from coroutine_callback(response)
        return response

    return new_callback


class HttpxClient(interfaces.HttpClientAdapter):
    exceptions = exceptions.Exceptions()

    def __init__(self, session=None, **kwargs):
        if httpx is None:
            raise NotImplementedError("httpx is not installed.")
        self._auto_created_session = False
        if session is None:
            session = httpx.AsyncClient(**kwargs)
            self._auto_created_session = True
        self._session = session
        self._sync_callback_adapter = threaded_callback

    def __del__(self):
        if self._auto_created_session:
            asyncio.get_event_loop().run_until_complete(self._session.aclose())

    @staticmethod
    @register.handler
    def with_session(session, *args, **kwargs):
        if isinstance(session, httpx.AsyncClient):
            return HttpxClient(session, *args, **kwargs)

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


HttpxClient.exceptions.ServerTimeout = httpx.ReadTimeout
