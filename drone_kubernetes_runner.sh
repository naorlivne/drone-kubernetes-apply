#!/usr/bin/env bash

# stop on first failure
set -e

# create the variable injected yaml config file
python drone_kubernetes_runner.py

# run kubectl apply on the variable injected yaml config file
kubectl --insecure-skip-tls-verify --server "${PLUGIN_KUBERNETES_API_HOST}" --token "${PLUGIN_KUBERNETES_TOKEN}" apply -f /tmp/injected_deployment.yaml
