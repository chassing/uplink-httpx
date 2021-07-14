import pytest
from uplink_httpx import HttpxClient

QUERY_PARAMS = [
    #
    ({"p": None}, {}),
    ({"p": "test"}, {"param": "test"}),
    ({"p": ["a", "b", 1]}, {"param": ["a", "b", "1"]}),
]


@pytest.mark.asyncio
async def test_consumer_header(client):
    async with client as session:
        r = await session.get()
        assert r["headers"]["Accept"] == "application/json"


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_get(client, args, expected):
    async with client as session:
        r = await session.get(**args)
    assert r["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_multiple_gets(client, args, expected):
    async with client as session:
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_reuse_client_and_multiple_gets(client, args, expected):
    async with client as session:
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected
    async with client as session:
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected
        assert (await session.get(**args))["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_post(client, args, expected, data):
    async with client as session:
        r = await session.post(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_patch(client, args, expected, data):
    async with client as session:
        r = await session.patch(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_put(client, args, expected, data):
    async with client as session:
        r = await session.put(body=data, **args)
    assert r["args"] == expected
    assert r["json"] == data


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_delete(client, args, expected):
    async with client as session:
        r = await session.delete(**args)
    assert r["args"] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("args, expected", QUERY_PARAMS)
async def test_consumer_multiple_methods(client, args, expected, data):
    async with client as session:
        # get
        assert (await session.get(**args))["args"] == expected
        # post
        r = await session.post(body=data, **args)
        assert r["args"] == expected
        assert r["json"] == data
        # patch
        r = await session.post(body=data, **args)
        assert r["args"] == expected
        assert r["json"] == data
        # delete
        r = await session.delete(**args)
        assert r["args"] == expected
        # final get
        assert (await session.get(**args))["args"] == expected


@pytest.mark.asyncio
async def test_consumer_timeout(client):
    with pytest.raises(HttpxClient.exceptions.ServerTimeout):
        async with client as session:
            await session.timeout()


@pytest.mark.asyncio
async def test_consumer_bad_status_code(client):
    with pytest.raises(HttpxClient.exceptions.BaseClientException):
        async with client as session:
            await session.status_code(400)
