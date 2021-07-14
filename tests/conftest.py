import pytest
import uplink
from uplink_httpx import ContextConsumer, HttpxClient

BASE_URL = "https://httpbin.org"


@uplink.response_handler
def raise_for_status(response):
    response.raise_for_status()
    return response


@raise_for_status
@uplink.timeout(10)
@uplink.headers({"Accept": "application/json"})
@uplink.returns.json()
class HttpBin(ContextConsumer):
    """Just a stub."""

    @uplink.get("get")
    def get(
        self,
        p: uplink.Query("param") = None,  # noqa: F821
    ):
        pass

    @uplink.get("/status/{code}")
    def status_code(self, code):
        pass

    @uplink.json
    @uplink.post("post")
    def post(
        self,
        body: uplink.Body(),
        p: uplink.Query("param") = None,  # noqa: F821
    ):
        pass

    @uplink.json
    @uplink.patch("patch")
    def patch(
        self,
        body: uplink.Body(),
        p: uplink.Query("param") = None,  # noqa: F821
    ):
        pass

    @uplink.json
    @uplink.put("put")
    def put(
        self,
        body: uplink.Body(),
        p: uplink.Query("param") = None,  # noqa: F821
    ):
        pass

    @uplink.delete("delete")
    def delete(
        self,
        p: uplink.Query("param") = None,  # noqa: F821
    ):
        pass

    @uplink.timeout(1)
    @uplink.get("delay/2")
    def timeout(self):
        pass


@pytest.fixture
def client():
    return HttpBin(base_url=BASE_URL, client=HttpxClient())


@pytest.fixture
def data():
    return {"a": 1, "b": ["test", "foo", 1], "c": "foo"}
