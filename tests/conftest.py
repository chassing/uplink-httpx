import sys

import uplink

import pytest
from uplink_httpx import HttpxClient

BASE_URL = "https://httpbin.org"


@uplink.headers({"Accept": "application/json"})
@uplink.returns.json()
class HttpBin(uplink.Consumer):
    """Just a stub."""

    @uplink.get("get")
    def get(self, p: uplink.Query("param") = None):
        pass

    @uplink.json
    @uplink.post("post")
    def post(self, body: uplink.Body(), p: uplink.Query("param") = None):
        pass

    @uplink.json
    @uplink.put("put")
    def put(self, body: uplink.Body(), p: uplink.Query("param") = None):
        pass

    @uplink.delete("delete")
    def delete(self, p: uplink.Query("param") = None):
        pass

    @uplink.get("delay/5")
    @uplink.timeout(2)
    def delay(self, p: uplink.Query("param") = None):
        pass


@pytest.fixture
def client():
    return HttpBin(base_url=BASE_URL, client=HttpxClient())
