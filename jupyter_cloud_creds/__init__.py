"""
A jupyter_server/notebook extension that helps provide temporary cloud provider
credentials by setting up an additional jupyter server endpoint for
authenticated users.
"""
from jupyter_server.utils import url_path_join

from ._version import __version__  # noqa
from .handlers import AWSCredentialsHandler


def _load_jupyter_server_extension(server_app):
    """
    This function is called when the extension is loaded.
    """
    base_url = server_app.web_app.settings["base_url"]
    server_app.web_app.add_handlers(
        ".*", [(url_path_join(base_url, "/api/jupyter-cloud-creds/aws"), AWSCredentialsHandler)]
    )


def _jupyter_server_extension_points():
    """
    Makes the jupyter_server singleuser extension discoverable.

    Returns a list of dictionaries with metadata describing
    where to find the `_load_jupyter_server_extension` function.

    ref: https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html
    """
    return [{"module": "jupyter_cloud_creds"}]


# For compatibility with notebook server, see
# https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html#migrating-an-extension-to-use-jupyter-server
load_jupyter_server_extension = _load_jupyter_server_extension
