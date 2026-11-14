#!/bin/bash
# Für die Lehrkraft: baut die Webseite (fragt nach dem Lösungs-Passwort) und überträgt den
# aktuellen Stand OHNE Lösungen und OHNE Probe-Server in das öffentliche Schüler-Repo
# (GitHub Pages aus docs/). Das Repo muss vorher existieren:
#   gh repo create bnBSinfo/rest_lernpfad_schueler --public
set -e
cd "$(dirname "$0")/.."
REPO=bnBSinfo/rest_lernpfad_schueler
python3 tool/seite_bauen.py
TMP=$(mktemp -d)
git clone -q "https://github.com/$REPO.git" "$TMP/repo" 2>/dev/null || true
[ -d "$TMP/repo/.git" ] || { mkdir -p "$TMP/repo"; git -C "$TMP/repo" init -q -b main; }
rsync -a --delete --exclude .git --exclude .dart_tool --exclude .idea --exclude .claude --exclude test \
  --exclude loesungen --exclude LEHRKRAFT.md --exclude 'tool/*.sh' --exclude tool/seite_bauen.py ./ "$TMP/repo/"
cd "$TMP/repo"
git add -A
git commit -q -m "Pi-Server & REST-API aktualisiert" || echo "Keine Änderungen."
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -q -u origin main
echo "Übertragen nach https://github.com/$REPO"
