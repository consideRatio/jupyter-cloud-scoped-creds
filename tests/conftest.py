import os

import pytest

os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

# pytest_jupyter ref: https://github.com/jupyter-server/pytest-jupyter
pytest_plugins = ["pytest_jupyter.jupyter_server"]

@pytest.fixture
def jp_server_config():
    yield {
        "ServerApp": {"jpserver_extensions": {"jupyter_cloud_creds": True}},
    }
