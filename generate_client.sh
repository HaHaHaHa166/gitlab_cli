#!/usr/bin/env bash
# Usage: ./generate_client.sh <openapi_spec_url_or_file>
SPEC_URL=${1:-"https://gitlab.com/gitlab-org/gitlab/-/raw/master/openapi/openapi.yaml"}
OUT_DIR=gitlab_openapi_client

docker run --rm -v "${PWD}:/local" openapitools/openapi-generator-cli generate \
  -i "${SPEC_URL}" \
  -g python \
  -o "/local/${OUT_DIR}" \
  --package-name openapi_client
