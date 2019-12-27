import pytest

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
