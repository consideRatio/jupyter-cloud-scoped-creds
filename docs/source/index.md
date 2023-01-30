<!--
This documentation is structured based on the Diataxis framework as described in
https://diataxis.fr/.

When writing documentation, consider these three personas:

- A system admin managing cloud resources and credentials (cloud admin)
- A user installing this package (environment admin)
- A user of the already installed package (end user)
-->

# jupyter-cloud-creds

TODO: project intro

TODO: document requirements and assumptions
    - aws / gcloud available
    - jupyterhub user server
    - network access to cloud metadata server

<!--
How-to guide ideas:
- Installing
- Acquire cloud creds from a browser
- Acquire cloud creds from a terminal
- Use cloud creds with `aws` CLI
- Use cloud creds with `gcloud` CLI
- Use cloud creds from Python
-->
```{toctree}
:caption: How-to guides
:maxdepth: 2
:glob:

how-to/*
```

<!--
Explanation topics:
- Cloud's access management (AWS IAM, GCP IAM)
- How cloud credentials present in user servers (AWS IRSA, GCP workload identity)
- How temporary credentials are acquired (aws sts assume-role-with-web-identity, gcp print-access-token)
-->
```{toctree}
:caption: How things work
:maxdepth: 2
:glob:

explanation/*
```

<!--
Tutorial ideas:
- Setup object storage access in GCP
- Setup object storage access in AWS
-->
```{toctree}
:caption: Tutorials
:maxdepth: 2
:glob:

tutorials/*
```

```{toctree}
:maxdepth: 2
:glob:

reference/*
```
