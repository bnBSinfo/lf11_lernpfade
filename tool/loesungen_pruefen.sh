#!/bin/sh
# Prüft Prüf-Tool und Musterlösungen gegen den Probe-Server (ohne echten Pi).
# Erwartet: Musterlösung 9/9 grün, Starter-Code Level 6, 7 und 9 rot.
set -e
cd "$(dirname "$0")/.."
TMP=$(mktemp -d)
trap 'kill $SRV 2>/dev/null; rm -rf "$TMP"' EXIT
dart run test/probe_server.dart 8088 2222 >/dev/null & SRV=$!
sleep 4
for art in loesung starter; do
  rm -rf "$TMP/p"; mkdir "$TMP/p"
  cp -R pubspec.yaml lib server tool "$TMP/p/"
  [ "$art" = loesung ] && cp -R loesungen/lib loesungen/server "$TMP/p/"
  printf 'ip=127.0.0.1\nhttp=8088\nssh=2222\n' > "$TMP/p/pi.txt"
  echo "== $art"
  (cd "$TMP/p" && dart pub get >/dev/null && dart run tool/pruefen.dart | tail -11)
done
