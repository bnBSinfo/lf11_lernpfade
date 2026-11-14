# Hinweise für die Lehrkraft

**Nicht an die Schüler weitergeben** – zusammen mit `loesungen/`, `test/` und `tool/*.sh`.
Die Schülerversion erzeugt `tool/schuelerversion_erstellen.sh` bzw. `tool/schueler_repo_aktualisieren.sh`.

Aufgebaut nach dem Muster der **Flutter-Einführung** (`flutter_lernpfad`): Level mit Auftrag, gestuften Tipps,
Merke und Denkfrage, Starter-Dateien mit `TODO`s, automatische Prüfung mit deutschen Hinweisen, Webseite mit
verschlüsselten Musterlösungen. Grundlage: `04__AP_LF11_BN_STO_RASP_DB_REST.docx`.

## Aufbau
| Ordner / Datei | Inhalt |
|---|---|
| `docs/level_0X.md`, `docs/bonus.md` | Auftrag, Erklärung, Tipps, Merke, Denkfrage |
| `pi.txt` | IP (und ggf. Ports) des Schüler-Pi |
| `server/sql/flutterdb.sql` | Level 6: Starter mit TODOs |
| `server/php/benutzer.php` | Level 7: Starter mit TODOs |
| `lib/todo_api.dart` | Level 9: Starter mit TODOs (später in der Flutter-App verwendbar) |
| `loesungen/` | Musterlösungen, gleiche Struktur |
| `tool/pruefen.dart` | Prüfung aller Level über das Netz (+ `level9_lauf.dart`, `pi_konfig.dart`) |
| `tool/todo_konsole.dart` | Spielwiese für Level 9 |
| `test/probe_server.dart` | simuliert einen fertigen Pi (HTTP + SSH-Banner) – **nicht für Schüler** |
| `tool/loesungen_pruefen.sh` | Lösungen 9/9 grün, Starter-Code Level 6/7/9 rot – gegen den Probe-Server |
| `tool/seite_bauen.py` | erzeugt `docs/index.html` (braucht pandoc, openssl) |

## Was die Prüfung kann – und was nicht
Das Tool fragt den Pi **von außen** ab, wie ein Test:
- L1 Pi antwortet unter der IP (auch „Connection refused“ zählt als erreichbar) · L2 SSH-Banner auf Port 22
- L3 Apache auf Port 80 · L4 `info.php` wird ausgeführt, `mysqli` geladen · L5 `/phpmyadmin/` liefert die Anmeldeseite
- L6 **nur statisch**: Inhalt von `flutterdb.sql` (Benutzer, `GRANT … flutterDB.*`, Primärschlüssel, ToDoTB, Beispieldaten)
- L7 Datei statisch (kein `SELECT *`, kein Passwort) **und** live: `/benutzer.php` liefert JSON mit berno/stoll ohne `passwordLogin`
- L8 php-crud-api: `records/flutterTB`, `records/flutterTB/1` (braucht PK), `records/ToDoTB`
- L9 die Schüler-Klasse `TodoApi` legt am Pi ein Prüf-ToDo an, hakt es ab und löscht es

Nicht prüfbar: SD-Karte, Benutzername, Updates. Wer die IP eines Nachbarn einträgt, ist bei L1–5 und L8 grün –
deshalb zur Abnahme `hostname` und `hostname -I` per SSH zeigen lassen (passt zum Abnahmeprotokoll).

## Änderungen gegenüber dem Skript (04__AP_LF11_BN_STO_RASP_DB_REST)
Vorschläge für die Überarbeitung des Skripts:
- **`flutterTB` ohne Primärschlüssel:** `id INT` ohne `PRIMARY KEY` – die php-crud-api findet dann `records/flutterTB/1`
  nicht. Im Lernpfad `id INT AUTO_INCREMENT PRIMARY KEY`.
- **`skripterstellung/flutter.sql`**: `GRANT … ON flutterDB TO` (ohne `.*`) – meint eine *Tabelle* flutterDB.
  Im .docx richtig. Außerdem fehlt dort `USE flutterDB;` vor `CREATE TABLE` im .docx.
- **Tabelle `ToDoTB`** wird im README erwähnt, im Skript aber nirgends angelegt – im Lernpfad mit
  `id, titel, erledigt` ergänzt (passt zur ToDo-Liste der Flutter-Einführung).
- **„Die 4 Ubuntu-Pakete“ in synaptic** sind nicht benannt → im Lernpfad per `apt`:
  `php libapache2-mod-php php-mysql` (L4) und `php-mbstring php-zip php-gd php-curl` (L5).
- `ifconfig`/`net-tools` ist veraltet → `hostname -I` (ifconfig als Alternative erwähnt).
- `systemctl enable --now ssh` fehlt – sonst startet SSH nicht überall automatisch.
- **REST-API als Download:** `docs/downloads/api.php` = Release v2.16.7 der php-crud-api (MIT, Lizenz liegt daneben),
  über GitHub Pages per `wget` abrufbar. Statt `git clone` – kein `.git`-Ordner im Webverzeichnis, feste Version.
  Aktualisieren: `gh release download <tag> -R mevdschee/php-crud-api -p api.php -D docs/downloads --clobber`.
- `gedit api.php` braucht einen Desktop, per SSH geht das nicht → `nano`.
- „php.info-Datei“ → die Datei heißt `info.php`. `nano`: Speichern ist Strg+O, Strg+X beendet (Skript: „strg x, Y“ – geht auch).
- Sicherheit (→ Bonus): Klartext-Passwörter, die API gibt `passwordLogin` aus, `info.php` bleibt liegen,
  `.git`-Ordner der php-crud-api ist im Web erreichbar.
- Tippfehler: Rasberry, SHH, RasB/Rasb, Datenabank, angeldegt, „Die Terminal“.

## Ablauf-Vorschlag
1. Flutter-Einführung abgeschlossen (Dart/Flutter installiert nach `02_AP_LF11_BN_STO_Installationsanleitung`).
2. Schüler erhalten das ZIP oder klonen das Schüler-Repo, `dart pub get`.
3. Je Level: Auftrag → am Pi umsetzen → `dart run tool/pruefen.dart <Level>` grün.
4. Stundenende: `dart run tool/pruefen.dart` – Ausgabe als Nachweis/Screenshot.
5. Ausblick (Bonus 1): `TodoApi` in die ToDo-App der Flutter-Einführung einbauen.

## Prüfen nach Änderungen
```
./tool/loesungen_pruefen.sh     # Lösung 9/9, Starter: 6, 7, 9 rot
dart analyze
```

## Schüler-Repo und Webseite
- Privat (dieses Repo, mit Lösungen): https://github.com/bnBSinfo/rest_lernpfad
- Öffentlich für Schüler (noch anzulegen): `gh repo create bnBSinfo/rest_lernpfad_schueler --public`,
  dann `./tool/schueler_repo_aktualisieren.sh` und in den Repo-Einstellungen GitHub Pages auf `main` / `docs` stellen.
- Lokal ansehen ohne Lösungen: `python3 tool/seite_bauen.py --ohne-loesungen` und `python3 -m http.server -d docs`.
- Die eingecheckte `docs/index.html` ist eine Vorschau **ohne** Lösungen; mit Passwort baut sie erst
  `schueler_repo_aktualisieren.sh`.

## Versionsnummer
Steht in `pubspec.yaml` (`version: 1.0.0+1`), erscheint auf der Webseite und in `dart run tool/pruefen.dart`.
Kleine Korrektur → `1.0.1`, neue Inhalte → `1.1.0`; die Zahl nach `+` jeweils um 1.
