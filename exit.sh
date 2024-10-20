#!/bin/bash

## be sure the file has right permissions
## chmod +x exit.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "Please source this script: source exit.sh"
  exit 1
fi

deactivate

echo "Virtual Environment is deactivated"