## AWS EKS

```{note}
The short version

A Pod referencing a k8s ServiceAccount with a EKS specific annotation
referencing an IAM Role gets mounted continuously refreshing AWS credentials
thanks to changes to the Pod specification made by a mutating webhook. These
credentials can be exported directly, but one can also acquire a token created
just in time with a known lifetime of one hour by default, up to possibly twelve
hours.
```

This page describes how AWS credentials can get setup for an AWS EKS cluster's
k8s Pod's containers via a k8s ServiceAccount and some EKS default machinery.

Let's assume we have a k8s ServiceAccount (SA) resource with an annotation
`eks.amazonaws.com/role-arn` referencing an IAM Role, like below:

```yaml
kind: ServiceAccount
metadata:
  name: my-serviceaccount-name
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/my-role-name
```

Let's then consider a Pod referencing the annotated k8s SA via
`serviceAccountName` like below is to be created through a request to the k8s
api-server:

```yaml
kind: Pod
# ...
spec:
  serviceAccountName: my-serviceaccount-name
  # ...
```

Before creation, the Pod will then get modified to look like this:

```yaml
kind: Pod
# ...
spec:
  serviceAccountName: my-serviceaccount-name
  # ...

  # Below are changes made by the mutating webhook
  volumes:
  - name: aws-iam-token
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          audience: sts.amazonaws.com
          expirationSeconds: 86400
          path: token
  containers:
    - # ...
      volumeMounts:
        - mountPath: /var/run/secrets/eks.amazonaws.com/serviceaccount
          name: aws-iam-token
          readOnly: true
      env:
        - name: AWS_STS_REGIONAL_ENDPOINTS
          value: regional
        - name: AWS_DEFAULT_REGION
          value: us-west-2
        - name: AWS_REGION
          value: us-west-2
        - name: AWS_ROLE_ARN  
          value: arn:aws:iam::123456789012:role/my-role-name
        - name: AWS_WEB_IDENTITY_TOKEN_FILE
          value: /var/run/secrets/eks.amazonaws.com/serviceaccount/token
```

This happens because the k8s api-server contacts a [mutating webhook] before the
Pod's creation is finalized, as the k8s api-server sees the
`MutatingWebhookConfiguration` resource named `pod-identity-webhook` setup in
AWS EKS clusters by default.

```yaml
# Redacted example from an EKS cluster versioned v1.29.6-eks-db838b0
kind: MutatingWebhookConfiguration
metadata:
  name: pod-identity-webhook
webhooks:
  - admissionReviewVersions:
      - v1beta1
    clientConfig:
      caBundle: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCmV4YW1wbGUKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=
      url: https://127.0.0.1:23443/mutate
    failurePolicy: Ignore
    matchPolicy: Equivalent
    name: iam-for-pods.amazonaws.com
    namespaceSelector: {}
    objectSelector: {}
    reinvocationPolicy: IfNeeded
    rules:
      - apiGroups:
          - ""
        apiVersions:
          - v1
        operations:
          - CREATE
        resources:
          - pods
        scope: '*'
    sideEffects: None
    timeoutSeconds: 10
```

The mutating webhook contacted by the k8s api-server is the
[amazon-eks-pod-identity-webhook].

The Pod's volume `aws-iam-token` mounted at
`/var/run/secrets/eks.amazonaws.com/serviceaccount/token` provides a
continuously updated AWS token, with a lifetime of 24 hours by default (the
webhook's defaults, can be overridden via a k8s ServiceAccount annotation). The
continuous updating is done by k8s machinery of a projected volume using a
[`serviceAccountToken` source]. Note that this functionality relies on having
the EKS cluster setup with OIDC (under `iam.withOIDC` in `eksctl` config).

This primary temporary token could be directly
extracted and used elsewhere by copying the token file and configuring
environment variables. This project isn't created to facilitate that though, but
instead to generate a secondary temporary token with the command `aws sts
assume-role-with-web-identity`.

A secondary temporary token generated with `assume-role-with-web-identity` will
expire after a fixed duration independently on the primary temporary token. By
default, these tokens will expire after one hour, but if requesting a longer
duration token explicitly and if the IAM Role allows it explicitly, the lifetime
can be extended to twelve hours. The lifetime can also be shorted, but to no
less than 15 minutes. For details, see the AWS docs about [credential
lifetimes].

[mutating webhook]: https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/
[amazon-eks-pod-identity-webhook]: https://github.com/aws/amazon-eks-pod-identity-webhook
[`serviceAccountToken` source]: https://kubernetes.io/docs/concepts/storage/projected-volumes/#serviceaccounttoken
[credential lifetimes]: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_manage-assume.html
