from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import APIHandler
#from jupyter_server.auth import authorized
from tornado import web
import asyncio

class CredentialHandler(APIHandler):

    @web.authenticated
    #@authorized
    async def get(self):
        """
        Calculate and return current resource usage metrics
        """
        cmd = ['pwd']
        # cmd = ['aws', 'sts', 'assume-role-with-web-identity',
        #        '--role-arn $AWS_ROLE_ARN',
        #        '--role-session-name $JUPYTERHUB_CLIENT_ID',
        #        '--web-identity-token file://$AWS_WEB_IDENTITY_TOKEN_FILE',
        #        '--duration-seconds 1000'
        #        ]

        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        self.write(stdout)


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
