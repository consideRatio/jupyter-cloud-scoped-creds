# jupyter-cloud-scoped-creds

When users log into JupyterHub on Kubernetes they can be given cloud provider credentials via a service account role. These permissions give access to resources like S3 buckets. Rather than making a bucket public, you can give authenticated users temporary to upload data files to object stores from any computer!

The goal of this server extension is to expose an API endpoint via a [Jupyter Server Extension](https://jupyter-server.readthedocs.io) that makes it easy for JupyterHub users to get temporary credentials:

```
https://HUBURL/user/YOURNAME/api/cloudcreds/aws
```

Returns something that looks like:
```
{
  "Credentials": {
    "AccessKeyId": "ASIAXXXXXXXXXXXXXXXXX",
    "SecretAccessKey": "XXXXXXXXXXXXXXXXXX",
    "SessionToken": "XXXXXXXX+ihPNZdQzj7aRtD080V42+TrZ/TtMsXAIgDNqz41KPfvsCYC/GZDJ9tB9aTUPt2ceXOuJKCg+ZP98q8gQIZhADGgw3ODMzODA4NTk1MjIiDOmodQHqEpP4IM9nKyrPBKW/8E2CdEOMN8jdk1yRRKC6RpZh70ADc9wkQpavHV6BSR+DpSyJciz2yHH2TNWCPmt3xsFldUp5R8/znla7fQDhFs+dsTlZ6zxvV86OxFDf5qc8yxaVkEport2F0dSdxwyMWh6bJWsSNcZy/YZY6HPQUU8BzNAY8uUybTzgwg7QFM+5p4l45tl+CejaJxUyu/xa95U5er9isivexcD5yGg8NfouTWvwvMeGbZdj2wRez3DCEeafiHfBAPHiTr1LIBtWvPkAbCEa38bfkRpSkxGaMBfjEbjbpoDKvQxXZLMWUjZWK53EliM7+ON8NCLFHAh8ggFw4y9KIYEyNmrnQ4OkZAFHMVAtCPyPs+61jtiGSwlSCyZNZJk1FYOOWIUrvnnAqrDYOacFBELSVGiDAEoCEQP6ePveGO+FfAiSZy5Zrv2mkHYfIq8hJzXOeCLeIg7gAxnxn64jrO6WP97TofLm9Nt7LHpho4R7xsGoTYsbwjmvDhN4HZCsvHnMc37oZJ0rKvLgTbb50cHLfJ8VJVqZZWBkFtxN14y7f3Y/GSN8Dm40n3jrSGRbEwrS8uI5db235hJRfw0L9FQ3TJg+6l/iSAtO4WmCO+C8MoTOmpxEwy5ETUnYYhf3ACnlKP3nIr7gV1M9BNewY/RuGvtquZZ1ZbHcDVhSl0gSTjJJ7e4jLVgsAHPsLq3s6p34r/aj3ah92DDChP9iF1sPSgMFXvBIqUtWaI5k/3kqoMic1QT55dhPdTEr+iQf+c4DvI4Wr967m9cdY6O2Ui8j+XNFaTCUkeyWBjqaAVMO/oSBOTMk8mPRqsRKmQzUiC8enQSkzMCr1/V9z4+pz5spjkFzEhXQro46vLvma4OyD2dAANuJ/NVFUmQxrbzfnGb3uxDh+V3g+ugdUOiFmhwDV5eCpaUxCnMOzRs/ieVpyzUljmtKDeTivP30IiJBkst7bqzQ/P+LcRu3eIhQgiAlqnkpyl3pxxk5Kt906DYLWFvr8gjMbI4=",
    "Expiration": "2022-07-22T20:45:48Z"
  },
  "SubjectFromWebIdentityToken": "system:serviceaccount:prod:pangeo",
  "AssumedRoleUser": {
    "AssumedRoleId": "XXXXXXXXXXXXXX:jupyterhub-user-scottyhq",
    "Arn": "arn:aws:sts::XXXXXXXXX:assumed-role/eksctl-pangeo-binder-addon-iamserviceaccount-Role1-1FIHHPOY6UU2A/jupyterhub-user-scottyhq"
  },
  "Provider": "arn:aws:iam::XXXXXXXXX:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/ACA8E0F49907CBD2E6E3388B0448A911",
  "Audience": "sts.amazonaws.com"
}
```

## How does it work?

Right now this only works for HUBs on AWS K8s that assign a service role for a user. The API endpoint just runs `aws sts assume-role-with-web-identity`
https://docs.aws.amazon.com/cli/latest/reference/sts/assume-role-with-web-identity.html


If you want to get credentials from another machine you can first go to https://HUBURL/user/YOURNAME/hub/token to get a token, then run:

```
curl https://HUBURL/api/cloudcreds/aws?token=0f5bf5fa97fe4ba0bb623226f0b33206
```

If you output the JSON returned to a file like `/tmp/irp-cred.txt` you can run the following commands in a terminal to set your credentials (requires `jq`):
```
export AWS_REGION="us-west-2"
export AWS_ACCESS_KEY_ID="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.AccessKeyId")"
export AWS_SECRET_ACCESS_KEY="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.SecretAccessKey")"
export AWS_SESSION_TOKEN="$(cat /tmp/irp-cred.txt | jq -r ".Credentials.SessionToken")"
```

## Roadmap
Developed quickly with Yuvi Panda at SciPy 2022!

Goal was to be as simple as possible, so no configuration options currently and it only works with AWS! But should be easy to extend to other Cloud providers

## Install
Install this in the Docker Image defining the JupyterHub environment for users
```
pip install git+https://github.com/scottyhq/jupyter-cloud-scoped-creds.git
```

## Local Development
```
pip install -e .
jupyter server
# go to http://localhost:8888/api/cloudcreds/aws
```
