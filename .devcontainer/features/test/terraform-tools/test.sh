#!/usr/bin/env bash

set -e

source dev-container-features-test-lib


check "tfswitch version" tfswitch --version
check "terraform version" /home/vscode/terraform-bin/terraform -version
check "terraform-docs version" terraform-docs --version
check "hclq version" hclq --version

reportResults
