# Hinweise für die Lehrkraft

Dieses Repo ist **öffentlich** und enthält alle drei LF11-Lernpfade (Musterlösungen, Abnahme-Werkzeug, Probe-Server). Die Schüler arbeiten mit der
Lernpfad-Seite – über mebis oder https://bnbsinfo.github.io/lf11_lernpfade/rest/.

Aufgebaut nach dem Muster der **Flutter-Einführung**: Level mit Auftrag, Erklärung, gestuften Tipps, Merke und
Denkfrage, Zielbild, Server-Stack, Datenfluss, Selbstkontrolle, verschlüsselte Musterlösungen.
Grundlage: `04__AP_LF11_BN_STO_RASP_DB_REST.docx`.

## Grundsatz: alles wird getippt
- Es gibt **keine Starter-Dateien und kein Projekt zum Importieren**. SQL (Level 6) und PHP (Level 7) schreiben die
  Schüler mit `nano` auf dem Pi, in Level 9 legen sie mit `dart create todo_client` ein eigenes Projekt an.
- Der Auftrag beschreibt, **was** das Programm tun soll; Code-Gerüste stehen nur in den Tipps.
- Auf der Seite ist Kopieren von Code gesperrt (nicht markierbar, Kopieren/Rechtsklick abgefangen, Hinweis
  „Bitte abtippen“). Ganz verhindern lässt sich das in keinem Browser – es soll vor allem bewusst machen.
- Einziger Download: die REST-API `api.php` (Level 8) – sie ist Werkzeug, kein Lerncode.

## Selbstkontrolle statt automatischer Tests
Je Level unter dem Auftrag: Checkliste „Das muss jetzt funktionieren“ (3–4 beobachtbare Ergebnisse) und
2 Kontrollfragen mit Feedback; die Falschantworten sind typische Fehler. Erst wenn alles abgehakt und richtig
beantwortet ist, lässt sich „Level geschafft“ setzen. Der Stand wird nur im Browser gespeichert (localStorage).
Inhalte: `tool/kontrolle.py`. Für einen späteren mebis-Test/H5P lassen sich die Fragen von dort übernehmen.

## Für mebis
`python3 tool/seite_bauen.py` (fragt das Lösungs-Passwort, mind. 10 Zeichen) erzeugt `docs/index.html`:
**eine einzige Datei**, Stylesheet, Schriften und Bilder sind eingebettet (ca. 0,8 MB). In mebis als *Datei*
hochladen (Anzeige: „Öffnen“/„Im neuen Fenster“) – oder auf die GitHub-Pages-Adresse verlinken.
Der Link zu `api.php` zeigt auf GitHub Pages; ist GitHub im Schulnetz gesperrt, `api.php` zusätzlich als
Datei in den mebis-Kurs legen.

## Aufbau des Repos
| Ordner / Datei | Inhalt |
|---|---|
| `docs/level_0X.md`, `docs/bonus.md` | Auftrag, Erklärung, Tipps, Merke, Denkfrage |
| `docs/downloads/api.php` | php-crud-api v2.16.7 (MIT, Lizenz daneben) |
| `tool/seite_bauen.py` | baut die Seite (braucht pandoc und openssl) |
| `tool/kontrolle.py` | Checklisten und Kontrollfragen je Level |
| `tool/lernpfad_bausteine.py` | Selbstkontrolle, Kopiersperre, Einbetten – identisch in der Flutter-Einführung |
| `tool/datenfluss.py`, `tool/wissen.html`, `tool/rest_baukasten.js` | Grafik, Wissen-Seite, REST-Baukasten |
| `loesungen/` | Musterlösungen: `server/sql/flutterdb.sql`, `server/php/benutzer.php`, `lib/todo_api.dart`, `bin/todo_client.dart` |
| `tool/pruefen.dart` + `pi.txt` | **Abnahme-Werkzeug** für Sie: prüft einen Schüler-Pi über das Netz |
| `test/probe_server.dart` | simuliert einen fertigen Pi (für Tests ohne Hardware) |
| `tool/loesungen_pruefen.sh` | Abnahme-Werkzeug und Musterlösung gegen den Probe-Server |
| `../veroeffentlichen.sh` | baut die Seite, legt sie nach `docs/` im Hauptordner und überträgt sie |

## Abnahme mit dem Werkzeug
IP des Schüler-Pi in `pi.txt` eintragen, dann `dart run tool/pruefen.dart` (Übersicht) oder `… 7` (ein Level).
- L1 Pi antwortet · L2 SSH-Banner · L3 Apache · L4 `info.php` mit mysqli · L5 phpMyAdmin
- L6 über die API (erst nach Level 8 möglich): ToDoTB mit Beispieldaten, Primärschlüssel in flutterTB
- L7 `/benutzer.php` liefert JSON mit berno/stoll ohne `passwordLogin`
- L8 php-crud-api: `records/flutterTB`, `records/flutterTB/1`, `records/ToDoTB`
- L9 legt mit der Musterlösung ein Prüf-ToDo an, hakt es ab und löscht es (prüft den Server, nicht den Schüler-Code –
  den lassen Sie sich mit `dart run bin/todo_client.dart <IP>` vorführen)
Zur Abnahme außerdem `hostname -I` per SSH zeigen lassen (sonst könnte die IP eines Nachbarn eingetragen sein).

## Änderungen gegenüber dem Skript (04__AP_LF11_BN_STO_RASP_DB_REST)
Vorschläge für die Überarbeitung des Skripts:
- **`flutterTB` ohne Primärschlüssel:** `id INT` ohne `PRIMARY KEY` – die php-crud-api findet dann `records/flutterTB/1`
  nicht. Im Lernpfad `id INT AUTO_INCREMENT PRIMARY KEY`.
- **`skripterstellung/flutter.sql`**: `GRANT … ON flutterDB TO` (ohne `.*`) – meint eine *Tabelle* flutterDB.
  Im .docx richtig. Außerdem fehlt im .docx `USE flutterDB;` vor `CREATE TABLE`.
- **Tabelle `ToDoTB`** wird im README erwähnt, im Skript aber nirgends angelegt – im Lernpfad mit
  `id, name, checkbox` ergänzt – Spaltennamen wie im Flutter-Skript (`ToDoListObject`, `webRequest.dart`).
- **„Die 4 Ubuntu-Pakete“ in synaptic** sind nicht benannt → im Lernpfad per `apt`:
  `php libapache2-mod-php php-mysql` (L4) und `php-mbstring php-zip php-gd php-curl` (L5).
- **REST-API als Download** statt `git clone`: feste Version, kein `.git`-Ordner im Webverzeichnis.
  Aktualisieren: `gh release download <tag> -R mevdschee/php-crud-api -p api.php -D docs/downloads --clobber`.
- `ifconfig`/`net-tools` ist veraltet → `hostname -I` (ifconfig als Alternative erwähnt).
- `systemctl enable --now ssh` fehlt – sonst startet SSH nicht überall automatisch.
- `gedit api.php` braucht einen Desktop, per SSH geht das nicht → `nano`.
- „php.info-Datei“ → die Datei heißt `info.php`. `nano`: Speichern ist Strg+O, Strg+X beendet.
- Sicherheit (→ Bonus): Klartext-Passwörter, die API gibt `passwordLogin` aus, `info.php` bleibt liegen.
- Tippfehler: Rasberry, SHH, RasB/Rasb, Datenabank, angeldegt, „Die Terminal“.

## Ablauf-Vorschlag
1. Flutter-Einführung abgeschlossen (Dart/Flutter installiert nach `02_AP_LF11_BN_STO_Installationsanleitung`).
2. Lernpfad-Seite in mebis öffnen, Pi bereitlegen.
3. Je Level: Auftrag → abtippen und umsetzen → Selbstkontrolle.
4. Abnahme stichprobenartig mit `dart run tool/pruefen.dart` und dem Abnahmeprotokoll.
5. Ausblick (Bonus 1): Lernpfad Flutter-Datenbankanbindung (https://bnbsinfo.github.io/lf11_lernpfade/datenbank/) – die ToDo-App nutzt dieselbe Tabelle `ToDoTB`.

## Prüfen nach Änderungen
```
./tool/loesungen_pruefen.sh     # 9/9 grün und ToDo-Liste vom Musterlösungs-Client
dart analyze
python3 tool/seite_bauen.py --ohne-loesungen && python3 -m http.server -d docs
```

## Versionsnummer
Steht in `pubspec.yaml`, erscheint auf der Seite. Kleine Korrektur → `x.y.1`, neue Inhalte → `x.1.0`;
die Zahl nach `+` jeweils um 1.
