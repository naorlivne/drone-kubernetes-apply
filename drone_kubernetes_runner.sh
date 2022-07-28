#!/usr/bin/env bash

# stop on first failure
set -e
set -x

# create the variable injected yaml config file
python /drone-kubernetes-apply/drone_kubernetes_runner.py


if [ -z "${PLUGIN_KUBERNETES_API_HOST}" ]
then
K8S_API_HOST=" "
else
K8S_API_HOST="--server ${PLUGIN_KUBERNETES_API_HOST}"
K8S_API_HOST="${K8S_API_HOST%\'}"
K8S_API_HOST="${K8S_API_HOST#\'}"
fi

if [ -z "${PLUGIN_KUBERNETES_TOKEN}" ]
then
K8S_TOKEN=" "
else
K8S_TOKEN="--token ${PLUGIN_KUBERNETES_TOKEN}"
K8S_TOKEN="${K8S_TOKEN%\'}"
K8S_TOKEN="${K8S_TOKEN#\'}"
fi

# run kubectl apply on the variable injected yaml config file
kubectl --insecure-skip-tls-verify ${K8S_API_HOST} ${K8S_TOKEN} apply -f /tmp/injected_deployment.yaml
