import logging

import uplink

log = logging.getLogger("uplink.httpx")


class ContextConsumer(uplink.Consumer):
    """Just a stub."""

    def __init__(self, *args, client=None, **kwargs):
        super().__init__(*args, client=client, **kwargs)
        self._client = client

    async def __aenter__(self):
        log.debug("ContextConsumer: __aenter__")
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        log.debug("ContextConsumer: __aexit__")
        await self._client.__aexit__()
