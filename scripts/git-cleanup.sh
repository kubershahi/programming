#!/bin/bash

GITHUB_DIR="$HOME/Documents/GitHub"

echo "Starting Git cleanup in: $GITHUB_DIR"
echo "--------------------------------------"

for repo in "$GITHUB_DIR"/*; do
  if [ -d "$repo/.git" ]; then
    echo ""
    echo "Repo: $(basename "$repo")"

    echo "Before:"
    du -sh "$repo/.git"

    cd "$repo" || continue

    git gc --prune=now
    git gc --aggressive

    echo "After:"
    du -sh .git
    echo "--------------------------------------"
  fi
done

echo "Done cleaning all repositories."