#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
    SED_COMMAND=gsed
    if command -v $SED_COMMAND > /dev/null 2>&1; then
        echo "Found gsed"
    else
        echo "GNU sed not installed. Try brew install gsed."
        exit 1
    fi
else
    SED_COMMAND=sed
fi

echo $SED_COMMAND
