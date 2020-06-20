# drone-kubernetes-apply

CI/CD build status: [![Build Status](https://cloud.drone.io/api/badges/naorlivne/drone-kubernetes-apply/status.svg)](https://cloud.drone.io/naorlivne/drone-kubernetes-apply)

Code coverage: [![codecov](https://codecov.io/gh/naorlivne/drone-kubernetes-apply/branch/master/graph/badge.svg)](https://codecov.io/gh/naorlivne/drone-kubernetes-apply)

Drone plugin for deploying to [kubernetes](https://kubernetes.io/) that allows injecting variables into the kubernetes YAML files & supports everything kubectl supports inside said YAML by running `kubectl apply` for you.

## Usage

This plugin can be used to deploy applications to a Kubernetes cluster, it will create\update the given kubernetes deployments/cron jobs/pods/etc as needed.

The below pipeline configuration demonstrates simple usage:

> In addition to the `.drone.yml` file you will need to create a `injected_deployment.yaml` file that contains the kubernetes configuration you want to deploy.

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: kubernetes_deploy
  image: naorlivne/drone-kubernetes-apply
  settings:
    kubernetes_token: my...vary...long...kube...token
    kubernetes_api_host: https://mykubecluster.example.com
    kubernetes_yaml_file: injected_deployment.yaml
```

### Value substitution

Example configuration with values substitution:
```yaml
kind: pipeline
type: docker
name: default

steps:
- name: kubernetes_deploy
  image: naorlivne/drone-kubernetes-apply
  settings:
    kubernetes_token: my...vary...long...kube...token
    kubernetes_api_host: https://mykubecluster.example.com
    kubernetes_yaml_file: injected_deployment.yaml
    my_image_tag: my_dynamic_image
```

In the `injected_deployment.yaml` file (please note the $ before the PLUGIN_MY_IMAGE_TAG key):

```yaml
{
  ...
  "image": "myrepo/myimage:$PLUGIN_MY_IMAGE_TAG",
  ...
}
```

will result in:

```yaml
{
  ...
  "image": "myrepo/myimage:my_dynamic_image",
  ...
}
```

## Parameter Reference

#### kubernetes_api_host

The kubernetes API server URL (no trailing slash should be used), alternately mount a kubeconfig into the container `/root/.kube/config`

#### kubernetes_token

The token used to auth against the kubernetes API, alternately mount a kubeconfig into the container `/root/.kube/config`

#### kubernetes_yaml_file

The kubernetes deployment configuration file location relative to the root folder of the repo, defaults to `injected_deployment.yaml`
