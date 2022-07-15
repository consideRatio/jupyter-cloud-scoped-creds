# jupyter-cloud-scoped-creds

When users log into JupyterHub on Kubernetes they can be given cloud provider credentials via a service account role. These permissions give access to resource like S3 buckets.

The goal of this server extension is to expose an API endpoint via a [Jupyter Server Extension](https://jupyter-server.readthedocs.io) that makes it easy for JupyterHub users to get temporary credentials.

This is useful for example to upload data files to object stores from a local computer!

## Install
Install this in the Docker Image defining the JupyterHub environment for users
```
pip install git+https://github.com/scottyhq/jupyter-cloud-scoped-creds.git
```

## Usage

Get environment variables to set for access
```
curl https://huburl.io/api/cloudcreds/aws
```

Set temporary credentials
```
export AWS_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.AccessKeyId")"
export AWS_SECRET_ACCESS_KEY="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.SecretAccessKey")"
export AWS_SESSION_TOKEN="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.SessionToken")"
```

## Roadmap
Developed quickly with Yuvi Panda at SciPy 2022!

Goal was to be as simple as possible, so no configuration options currently and it only works with AWS! But should be easy to extend to other Cloud providers

### Issues
Hmmm...
* [W 2022-07-14 17:48:13.154 ServerApp] Content security violation: {"csp-report":{"document-uri":"http://127.0.0.1:8889/api/cloudcreds/aws","referrer":"","violated-directive":"style-src-attr","effective-directive":"style-src-attr","original-policy":"frame-ancestors 'self'; report-uri /api/security/csp-report; default-src 'none'","blocked-uri":"inline","status-code":200}}
