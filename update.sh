#!/bin/bash
if ! git diff --quiet origin/master; then
    git pull master
    printf "Updated Cuteplayer!\n"
    exit 1
else
    printf "Cuteplayer up-to-date."
    exit 0
fi
