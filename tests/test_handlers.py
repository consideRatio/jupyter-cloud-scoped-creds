async def test_get(jp_fetch):
    response = await jp_fetch("api/jupyter-cloud-creds/aws")
    assert response.code == 200
