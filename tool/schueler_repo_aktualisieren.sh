#!/bin/bash
# Für die Lehrkraft: baut die eigenständige Lernpfad-Seite (fragt nach dem Lösungs-Passwort) und
# überträgt NUR docs/ (Seite + Downloads wie api.php) ins öffentliche Repo – GitHub Pages zeigt sie an.
# Mit --ohne-loesungen: Seite ohne Musterlösungen.
set -e
cd "$(dirname "$0")/.."
REPO=bnBSinfo/rest_lernpfad_schueler
python3 tool/seite_bauen.py "$@"
TMP=$(mktemp -d)
git clone -q "https://github.com/$REPO.git" "$TMP/repo" 2>/dev/null || true
[ -d "$TMP/repo/.git" ] || { mkdir -p "$TMP/repo"; git -C "$TMP/repo" init -q -b main; }
find "$TMP/repo" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
mkdir -p "$TMP/repo/docs"
rsync -a docs/index.html docs/.nojekyll docs/downloads "$TMP/repo/docs/"
cat > "$TMP/repo/README.md" <<'TXT'
# Pi-Server & REST-API – Lernpfad LF11

Die Lernpfad-Seite: https://bnbsinfo.github.io/rest_lernpfad_schueler/

Alles wird selbst getippt – es gibt bewusst keine Vorlagen zum Herunterladen.
Einziger Download: die REST-API `docs/downloads/api.php` (php-crud-api, MIT-Lizenz) für Level 8.
TXT
cd "$TMP/repo"
git add -A
git commit -q -m "Pi-Server & REST-API aktualisiert" || echo "Keine Änderungen."
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -q -u origin main
echo "Übertragen nach https://github.com/$REPO"
