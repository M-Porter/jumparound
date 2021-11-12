#!/usr/bin/env bash

git rev-parse 2> /dev/null
# shellcheck disable=SC2181
if [[ "$?" != "0" ]]; then
    echo "not in a git dir" && exit 1
fi

git config "core.hooksPath" "scripts/hooks"
