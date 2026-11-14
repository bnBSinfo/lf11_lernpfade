#!/bin/sh
# Prüft Abnahme-Werkzeug und Musterlösung (Dart-Client) gegen den Probe-Server (ohne echten Pi).
# Erwartet: 9/9 Level grün und eine ToDo-Liste vom Client.
set -e
cd "$(dirname "$0")/.."
trap 'kill $SRV 2>/dev/null; [ -f pi.txt.bak ] && mv pi.txt.bak pi.txt' EXIT
dart run test/probe_server.dart 8088 2222 >/dev/null & SRV=$!
sleep 4
[ -f pi.txt ] && cp pi.txt pi.txt.bak
printf 'ip=127.0.0.1\nhttp=8088\nssh=2222\n' > pi.txt
dart run tool/pruefen.dart | tail -11
echo "== Musterlösung todo_client"
dart run loesungen/bin/todo_client.dart 127.0.0.1:8088 neu "Test aus Dart"
dart run loesungen/bin/todo_client.dart 127.0.0.1:8088 weg 4 | tail -2
