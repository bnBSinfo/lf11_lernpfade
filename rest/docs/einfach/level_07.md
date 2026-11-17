# Level 7 – Eine eigene PHP-Schnittstelle

**Ziel:** Ein kleines PHP-Programm liest die Benutzer aus der Datenbank. Es gibt sie als **JSON** aus. Ohne Passwörter.

**Du schreibst:** `/var/www/html/benutzer.php` auf dem Pi · **Skript:** Schnittstelle zur Datenbank erstellen

## Auftrag
**📄 Neue Datei** `/var/www/html/benutzer.php`. Lege sie auf dem Pi an:
{{code 0}}
Das Programm macht diese 5 Dinge. Halte die Reihenfolge ein:

1. Es sagt: Jetzt kommt JSON. Header: `Content-Type: application/json; charset=utf-8`.
2. Es verbindet sich mit MySQL. Rechner `localhost`. Benutzer, Passwort und Datenbank aus Level 6.
3. Klappt die Verbindung nicht? Dann Statuscode 500 und `{"fehler": "Keine Verbindung zur Datenbank"}`. Dann Schluss.
4. Es liest aus `flutterTB` **nur** `id` und `name`. Sortiert nach `id`.
5. Es holt alle Zeilen als Liste. Es gibt sie als JSON aus.

**🌐 Browser** Öffne dann `http://<IP>/benutzer.php`. Firefox zeigt das JSON schön an.

## Profi-Auftrag
- `http://<IP>/benutzer.php` gibt `id` und `name` aller Benutzer als JSON aus. **Ohne** Passwörter.
- Content-Type ist JSON. Die Verbindung läuft über `flutterUser`.
- Ohne Verbindung: Statuscode 500 und eine Fehlermeldung als JSON.

## Erklärt – was passiert hier?

{{code 1}}

| Baustein | Was er macht |
|---|---|
| `header('Content-Type: …');` | sagt: Hier kommt JSON |
| `$db = new mysqli(host, user, pw, db);` | verbindet mit der Datenbank |
| `$db->connect_errno` | ist nicht 0, wenn die Verbindung nicht geht |
| `http_response_code(500);` | setzt den Statuscode |
| `$ergebnis = $db->query('SELECT …');` | schickt SQL an MySQL |
| `$ergebnis->fetch_all(MYSQLI_ASSOC)` | holt alle Zeilen als Liste |
| `echo json_encode($liste);` | macht JSON daraus und gibt es aus |

**JSON** ist das Format zwischen Server und App. `[ ]` ist eine Liste. `{ }` ist ein Objekt.

**Nur id und name:** Jeder im Netz kann die Antwort lesen. Darum nie `SELECT *`. Und nie Passwörter.

**PHP-Regeln:** Jede Datei beginnt mit `<?php`. Jede Anweisung endet mit `;`. Variablen beginnen mit `$`. Schreib das Passwort in **einfache** Anführungszeichen. Sonst liest PHP `$$` als Variable.

<details><summary>Tipp 1 – Gerüst</summary>

{{code 2}}
</details>

<details><summary>Tipp 2 – HTTP 500 oder weiße Seite</summary>

Der Fehler steht im Log: `tail /var/log/apache2/error.log`. „Access denied“ heißt: Zugangsdaten falsch. „Table doesn't exist“ heißt: Level 6 fehlt. „syntax error“ heißt: Tippfehler, oft fehlt ein `;`.
</details>

> **Merke:** Eine Schnittstelle gibt Daten in einem festen Format heraus. Und nur die Daten, die gebraucht werden.

**Denkfrage:** Für jede Tabelle und jede Aktion eine eigene PHP-Datei. Wie viele Dateien sind das bei 10 Tabellen? Was wäre besser?
