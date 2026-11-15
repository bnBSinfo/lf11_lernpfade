#!/bin/bash
# Baut einen oder alle Lernpfade (fragt jeweils das Lösungs-Passwort), legt die Seite nach docs/ und überträgt sie.
#   ./veroeffentlichen.sh flutter|datenbank|rest|alle [--ohne-loesungen]
# GitHub Pages zeigt docs/: https://bnbsinfo.github.io/lf11_lernpfade/
set -e
cd "$(dirname "$0")"
WAS=${1:-alle}; shift || true
bauen() {
  case "$1" in
    flutter)   python3 flutter_einfuehrung/tool/seite_bauen.py "${@:2}" && Q=flutter_einfuehrung/docs ;;
    datenbank) python3 flutter_datenbank/seite_bauen.py && Q=flutter_datenbank/docs ;;
    rest)      python3 rest/tool/seite_bauen.py "${@:2}" && Q=rest/docs
               mkdir -p docs/rest && rsync -a rest/docs/downloads docs/rest/ ;;
    *) echo "Unbekannt: $1 (flutter|datenbank|rest|alle)"; exit 1 ;;
  esac
  mkdir -p "docs/$1" && cp "$Q/index.html" "docs/$1/index.html"
}
if [ "$WAS" = alle ]; then for x in flutter datenbank rest; do bauen $x "$@"; done; else bauen "$WAS" "$@"; fi
touch docs/.nojekyll
git add -A
git commit -q -m "Seiten veröffentlicht: $WAS" || echo "Keine Änderungen."
git push -q
echo "Online in 1–2 Minuten: https://bnbsinfo.github.io/lf11_lernpfade/"
