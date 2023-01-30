import asyncio
import os

from jupyter_server.base.handlers import APIHandler
from tornado import web

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
