import pytest
from uplink_httpx import HttpxClient

QUERY_PARAMS = [
    #
    ({"p": None}, {}),
    ({"p": "test"}, {"param": "test"}),
    ({"p": ["a", "b", 1]}, {"param": ["a", "b", "1"]}),
]


@pytest.mark.asyncio
async def test_header(client):
    r = await client.get()
    assert r["headers"]["Accept"] == "application/json"


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_get(client, args, expected):
    r = await client.get(**args)
    assert r["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_multiple_gets(client, args, expected):
    assert (await client.get(**args))["args"] == expected
    assert (await client.get(**args))["args"] == expected
    assert (await client.get(**args))["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_post(client, args, expected, data):
    r = await client.post(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_patch(client, args, expected, data):
    r = await client.patch(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_put(client, args, expected, data):
    r = await client.put(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_delete(client, args, expected):
    r = await client.delete(**args)
    assert r["args"] == expected


@pytest.mark.asyncio
async def test_timeout(client):
    with pytest.raises(HttpxClient.exceptions.ServerTimeout):
        await client.timeout()


@pytest.mark.asyncio
async def test_bad_status_code(client):
    with pytest.raises(HttpxClient.exceptions.BaseClientException):
        await client.status_code(400)
