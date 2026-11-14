#!/bin/bash
# Für die Lehrkraft: erzeugt rest_lernpfad_schueler.zip ohne Lösungen und ohne Probe-Server.
set -e
cd "$(dirname "$0")/.."
ZIEL="$(pwd)/../rest_lernpfad_schueler.zip"
TMP=$(mktemp -d)/rest_lernpfad
mkdir -p "$TMP"
rsync -a --exclude .dart_tool --exclude .git --exclude .idea --exclude .claude --exclude test \
  --exclude loesungen --exclude LEHRKRAFT.md --exclude 'tool/*.sh' --exclude tool/seite_bauen.py ./ "$TMP/"
rm -f "$ZIEL"
(cd "$(dirname "$TMP")" && zip -qr "$ZIEL" rest_lernpfad)
rm -rf "$(dirname "$TMP")"
echo "Erstellt: $ZIEL"
