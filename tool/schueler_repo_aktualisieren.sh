#!/bin/bash
# Für die Lehrkraft: überträgt den aktuellen Stand OHNE Lösungen in das
# öffentliche Schüler-Repo (mit GitHub-Pages-Seite aus docs/).
set -e
cd "$(dirname "$0")/.."
REPO=bnBSinfo/flutter_lernpfad_schueler
python3 tool/seite_bauen.py
TMP=$(mktemp -d)
git clone -q "https://github.com/$REPO.git" "$TMP/repo" 2>/dev/null || true
[ -d "$TMP/repo/.git" ] || { mkdir -p "$TMP/repo"; git -C "$TMP/repo" init -q -b main; }
rsync -a --delete --exclude .git --exclude build --exclude .dart_tool --exclude .idea \
  --exclude loesungen --exclude LEHRKRAFT.md --exclude 'tool/*.sh' --exclude tool/seite_bauen.py \
  --exclude ephemeral --exclude flutter_export_environment.sh --exclude Generated.xcconfig \
  --exclude local.properties ./ "$TMP/repo/"
cd "$TMP/repo"
git add -A
git commit -q -m "Lernpfad aktualisiert" || echo "Keine Änderungen."
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -q -u origin main
echo "Übertragen nach https://github.com/$REPO"
