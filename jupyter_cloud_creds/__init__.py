"""
A jupyter_server/notebook extension that helps provide temporary cloud provider
credentials by setting up an additional jupyter server endpoint for
authenticated users.
"""
import asyncio
import os

from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from tornado import web

from .version import __version__  # noqa

class AWSCredentialsHandler(APIHandler):
    @web.authenticated
    async def get(self):
        """
        Acquire and return temporary AWS role credentials by exchanging a k8s
        issued token.

        To understand how this works, see:
        - A blog post introducing this: https://aws.amazon.com/blogs/opensource/introducing-fine-grained-iam-roles-service-accounts/
        - aws CLI, command instructions: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html#cli-configure-role-oidc
        - aws CLI, command reference: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/assume-role-with-web-identity.html
        """
        cmd = [
            "aws",
            "sts",
            "assume-role-with-web-identity",
            f"--role-arn={os.environ['AWS_ROLE_ARN']}",
            f"--role-session-name={os.environ['JUPYTERHUB_CLIENT_ID']}",
            f"--web-identity-token=file://{os.environ['AWS_WEB_IDENTITY_TOKEN_FILE']}",
            "--duration-seconds=1000",
        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await proc.communicate()

        self.write(stdout)
        self.write(stderr)  # For testing/debugging


def _load_jupyter_server_extension(server_app):
    """
    This function is called when the extension is loaded.
    """
    base_url = server_app.web_app.settings["base_url"]
    server_app.web_app.add_handlers(
        ".*", [(url_path_join(base_url, "/api/cloudcreds/aws"), AWSCredentialsHandler)]
    )


def _jupyter_server_extension_points():
    """
    Returns a list of dictionaries with metadata describing
    where to find the `_load_jupyter_server_extension` function.
    """
    return [{"module": "jupyter_cloud_creds"}]


# For compatibility with notebook server, see
# https://jupyter-server.readthedocs.io/en/latest/developers/extensions.html#migrating-an-extension-to-use-jupyter-server
load_jupyter_server_extension = _load_jupyter_server_extension
