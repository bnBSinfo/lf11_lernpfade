#!/bin/bash
# Für die Lehrkraft: prüft, ob alle Musterlösungen die Tests bestehen.
set -e
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
rsync -a --exclude build --exclude .dart_tool ./ "$TMP/"
rsync -a loesungen/lib/ "$TMP/lib/"
cd "$TMP" && flutter test --reporter compact 2>&1 | tail -3
rm -rf "$TMP"
