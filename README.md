# Pi-Server & REST-API – Lernpfad LF11

In 9 Leveln richten Sie einen Raspberry Pi als Datenbankserver mit REST-API ein – und sprechen ihn am Ende aus Dart an,
so wie später Ihre Flutter-App. Fortsetzung der **Flutter-Einführung**.

## Start
1. Projekt in VS Code oder Android Studio öffnen, einmalig: `dart pub get`
2. Level-Anleitung auf der Webseite oder in `docs/level_0X.md` lesen und am Pi umsetzen.
3. In `pi.txt` die IP-Adresse Ihres Pi eintragen (Level 1).
4. Prüfen:
   ```
   dart run tool/pruefen.dart       # Übersicht über alle Level
   dart run tool/pruefen.dart 4     # ein Level ausführlich mit Hinweisen
   ```

## Ihre Dateien
| Level | Datei | Was Sie tun |
|---|---|---|
| 1 | `pi.txt` | IP-Adresse eintragen |
| 6 | `server/sql/flutterdb.sql` | SQL-TODOs ergänzen, auf dem Pi ausführen |
| 7 | `server/php/benutzer.php` | PHP-TODOs ergänzen, nach `/var/www/html` kopieren |
| 8 | `docs/downloads/api.php` | REST-API (php-crud-api) – auf den Pi laden, Zugangsdaten eintragen |
| 9 | `lib/todo_api.dart` | Dart-TODOs ergänzen, ausprobieren mit `dart run tool/todo_konsole.dart` |

Level 1–5 und 8 erledigen Sie direkt auf dem Pi (Terminal / SSH).
