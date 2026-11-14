# Level 7 – Eine eigene PHP-Schnittstelle

**Ziel:** Ein kleines PHP-Programm liest die Benutzer aus der Datenbank und gibt sie als **JSON** aus – ohne Passwörter.

**Dateien:** `server/php/benutzer.php` · **Skript:** Schnittstelle zur Datenbank erstellen

## Auftrag
1. Ergänzen Sie in `server/php/benutzer.php` die **TODOs 1–4**.
2. Kopieren Sie die Datei auf den Pi:
   ```bash
   scp server/php/benutzer.php administrator@<IP>:/tmp/     # auf dem PC
   cp /tmp/benutzer.php /var/www/html/                      # auf dem Pi
   ```
3. Öffnen Sie `http://<IP>/benutzer.php` im Browser – Firefox zeigt das JSON übersichtlich an.

## Erklärt – was passiert hier?

```text
Browser ──GET /benutzer.php──▶ Apache ──▶ PHP ──SQL──▶ MySQL
        ◀── [{"id":1,"name":"berno"}, …] ── json_encode ◀── Zeilen
```

| Zeile | Bedeutung |
|---|---|
| `header('Content-Type: application/json; …')` | sagt dem Empfänger: hier kommt JSON, kein HTML |
| `new mysqli(host, user, pw, db)` | öffnet die Verbindung mit den Zugangsdaten aus Level 6 |
| `$db->query('SELECT …')` | schickt SQL an MySQL |
| `fetch_all(MYSQLI_ASSOC)` | holt alle Zeilen als Liste von Arrays `['id' => 1, 'name' => 'berno']` |
| `json_encode(...)` | macht daraus Text im JSON-Format |

**JSON** ist das Austauschformat zwischen Server und App: `[ ]` = Liste, `{ }` = Objekt mit `"schlüssel": wert`. Ihre Flutter-App kann es mit `jsonDecode` direkt in Dart-Listen und -Maps verwandeln.

**Nur id und name:** Was die Schnittstelle ausgibt, kann jeder im Netz lesen. Deshalb nie `SELECT *` – und nie Passwörter.

## Prüfen
`dart run tool/pruefen.dart 7` – erst die Datei auf Ihrem PC, dann die Antwort vom Pi.

<details><summary>Tipp 1 – TODO 2 und 3</summary>

```php
$db = new mysqli('localhost', 'flutterUser', 'Pa$$w0rd', 'flutterDB');
$ergebnis = $db->query('SELECT id, name FROM flutterTB ORDER BY id');
```
In PHP stehen Variablen mit `$` – im Passwort in **einfachen** Anführungszeichen ist `$$` deshalb harmlos.
</details>

<details><summary>Tipp 2 – HTTP 500 / weiße Seite</summary>

Die Fehlermeldung steht im Log des Webservers: `tail /var/log/apache2/error.log`. „Access denied“ = Zugangsdaten falsch, „Table doesn't exist“ = Level 6 nicht ausgeführt.
</details>

> **Merke:** Eine Schnittstelle (API) gibt Daten in einem festen Format (JSON) heraus – und nur die Daten, die der Empfänger wirklich braucht.

**Denkfrage:** Für jede Tabelle und jede Aktion (lesen, anlegen, ändern, löschen) eine eigene PHP-Datei – wie viele Dateien wären das für 10 Tabellen? Was wäre besser? (→ Level 8)
