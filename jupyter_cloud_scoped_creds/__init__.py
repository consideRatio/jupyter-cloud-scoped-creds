from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import APIHandler
from tornado import web
import asyncio
import os

class CredentialHandler(APIHandler):

    @web.authenticated
    async def get(self):
        """
        Calculate and return current resource usage metrics
        """
        # cmd = ['pwd'] # For testing/debugging

        cmd = ['aws', 'sts', 'assume-role-with-web-identity',
               '--role-arn', os.environ['AWS_ROLE_ARN'],
               '--role-session-name', os.environ['JUPYTERHUB_CLIENT_ID'],
               '--web-identity-token', f'file://{os.environ["AWS_WEB_IDENTITY_TOKEN_FILE"]}',
               '--duration-seconds', '1000'
               ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        self.write(stdout)
        self.write(stderr) # For testing/debugging


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]
    server_app.web_app.add_handlers(
        ".*", [(url_path_join(base_url, "/api/cloudcreds/aws"), CredentialHandler)]
    )

def _jupyter_server_extension_points():
    """
    Set up the server extension for collecting metrics
    """
    return [{"module": "jupyter_cloud_scoped_creds"}]
