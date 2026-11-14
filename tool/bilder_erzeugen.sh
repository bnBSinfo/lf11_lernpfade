#!/bin/bash
# Für die Lehrkraft: erzeugt docs/bilder/*.png aus den Musterlösungen.
set -e
cd "$(dirname "$0")/.."
export MATERIAL_FONTS="$(dirname "$(readlink -f "$(which flutter)")")/cache/artifacts/material_fonts"
TMP=$(mktemp -d)
rsync -a --exclude build --exclude .dart_tool --exclude .git ./ "$TMP/"
rsync -a loesungen/lib/ "$TMP/lib/"
cp loesungen/screenshots/screenshots_test.dart "$TMP/test/"
(cd "$TMP" && flutter test test/screenshots_test.dart --update-goldens --reporter compact 2>&1 | tail -1)
mkdir -p docs/bilder && cp "$TMP"/test/bilder/*.png "$TMP"/test/bilder/marken.json docs/bilder/
rm -rf "$TMP"
ls docs/bilder
