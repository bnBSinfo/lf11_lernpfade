#!/bin/bash
# Für die Lehrkraft: baut die eigenständige Lernpfad-Seite (fragt nach dem Lösungs-Passwort) und
# überträgt NUR die Seite ins öffentliche Repo – GitHub Pages zeigt sie an.
# Mit --ohne-loesungen: Seite ohne Musterlösungen.
set -e
cd "$(dirname "$0")/.."
REPO=bnBSinfo/flutter_lernpfad_schueler
python3 tool/seite_bauen.py "$@"
TMP=$(mktemp -d)
git clone -q "https://github.com/$REPO.git" "$TMP/repo" 2>/dev/null || true
[ -d "$TMP/repo/.git" ] || { mkdir -p "$TMP/repo"; git -C "$TMP/repo" init -q -b main; }
# Alles außer .git und docs/ entfernen; in docs/ nur die Dateien der Einführung ersetzen.
# Unterordner wie docs/datenbank/ (eigene Lernpfad-Pakete) bleiben erhalten.
find "$TMP/repo" -mindepth 1 -maxdepth 1 ! -name .git ! -name docs -exec rm -rf {} +
mkdir -p "$TMP/repo/docs"
find "$TMP/repo/docs" -mindepth 1 -maxdepth 1 -type f -exec rm -f {} +
rsync -a docs/index.html docs/.nojekyll "$TMP/repo/docs/"
cat > "$TMP/repo/README.md" <<'TXT'
# Flutter-Einführung LF11

Die Lernpfad-Seite: https://bnbsinfo.github.io/flutter_lernpfad_schueler/

Alles wird selbst getippt – es gibt bewusst kein Projekt zum Herunterladen.
In Level 1 legen Sie mit `flutter create meine_app` Ihr eigenes Projekt an.

## Fortsetzung: Datenbankanbindung

https://bnbsinfo.github.io/flutter_lernpfad_schueler/datenbank/

In 6 Leveln binden Sie Ihre App an den Pi aus dem REST-Lernpfad an – erst die Login-Maske, dann die ToDo-Liste.
TXT
cd "$TMP/repo"
git add -A
git commit -q -m "Flutter-Einführung aktualisiert" || echo "Keine Änderungen."
git remote get-url origin >/dev/null 2>&1 || git remote add origin "https://github.com/$REPO.git"
git push -q -u origin main
echo "Übertragen nach https://github.com/$REPO"
