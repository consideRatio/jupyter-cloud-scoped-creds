from http import HTTPStatus

async def test_aws_handler_not_setup(jp_fetch):
    response = await jp_fetch("api", "jupyter-cloud-creds", "aws", raise_error=False)
    assert response.code == HTTPStatus.SERVICE_UNAVAILABLE
