#!/bin/bash
# Für die Lehrkraft: erzeugt flutter_lernpfad_schueler.zip ohne Lösungen.
set -e
cd "$(dirname "$0")/.."
ZIEL="$(pwd)/../flutter_lernpfad_schueler.zip"
TMP=$(mktemp -d)/flutter_lernpfad
mkdir -p "$TMP"
rsync -a --exclude build --exclude .dart_tool --exclude .git --exclude .idea \
  --exclude loesungen --exclude LEHRKRAFT.md --exclude 'tool/*.sh' --exclude ephemeral --exclude flutter_export_environment.sh --exclude Generated.xcconfig --exclude local.properties ./ "$TMP/"
rm -f "$ZIEL"
(cd "$(dirname "$TMP")" && zip -qr "$ZIEL" flutter_lernpfad)
rm -rf "$(dirname "$TMP")"
echo "Erstellt: $ZIEL"
