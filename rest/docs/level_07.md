# Level 7 – Eine eigene PHP-Schnittstelle

**Ziel:** Ein kleines PHP-Programm liest die Benutzer aus der Datenbank und gibt sie als **JSON** aus – ohne Passwörter.

**Sie schreiben:** `/var/www/html/benutzer.php` auf dem Pi · **Skript:** Schnittstelle zur Datenbank erstellen

## Auftrag
Legen Sie auf dem Pi die Datei an:
```bash
nano /var/www/html/benutzer.php
```
Das Programm soll – in dieser Reihenfolge:

1. dem Empfänger mitteilen, dass JSON kommt: Header `Content-Type: application/json; charset=utf-8`,
2. eine Verbindung zu MySQL öffnen – Rechner `localhost`, Benutzer, Passwort und Datenbank aus Level 6,
3. bei einem Verbindungsfehler den Statuscode 500 und `{"fehler": "Keine Verbindung zur Datenbank"}` ausgeben und aufhören,
4. aus `flutterTB` **nur** `id` und `name` lesen, sortiert nach `id`,
5. alle Zeilen als Liste holen und als JSON ausgeben.

Öffnen Sie dann `http://<IP>/benutzer.php` im Browser – Firefox zeigt das JSON übersichtlich an.

## Erklärt – was passiert hier?

```text
Browser ──GET /benutzer.php──▶ Apache ──▶ PHP ──SQL──▶ MySQL
        ◀── [{"id":1,"name":"berno"}, …] ── json_encode ◀── Zeilen
```

| Baustein | Bedeutung |
|---|---|
| `header('Content-Type: …');` | sagt dem Empfänger: hier kommt JSON, kein HTML |
| `$db = new mysqli(host, user, pw, db);` | öffnet die Verbindung |
| `$db->connect_errno` | ist ungleich 0, wenn die Verbindung fehlschlug |
| `http_response_code(500);` | setzt den Statuscode |
| `$ergebnis = $db->query('SELECT …');` | schickt SQL an MySQL |
| `$ergebnis->fetch_all(MYSQLI_ASSOC)` | holt alle Zeilen als Liste von Arrays `['id' => 1, 'name' => 'berno']` |
| `echo json_encode($liste);` | macht daraus JSON-Text und gibt ihn aus |

**JSON** ist das Austauschformat zwischen Server und App: `[ ]` = Liste, `{ }` = Objekt mit `"schlüssel": wert`. Ihre Flutter-App verwandelt es mit `jsonDecode` direkt in Dart-Listen und -Maps.

**Nur id und name:** Was die Schnittstelle ausgibt, kann jeder im Netz lesen. Deshalb nie `SELECT *` – und nie Passwörter.

**PHP-Regeln:** Jede Datei beginnt mit `<?php`, jede Anweisung endet mit `;`, Variablen beginnen mit `$`. Im Passwort in **einfachen** Anführungszeichen ist `$$` deshalb harmlos – in doppelten würde PHP es als Variable lesen.

<details><summary>Tipp 1 – Gerüst</summary>

```php
<?php
header(…);

$db = new mysqli(…, …, …, …);
if ($db->connect_errno) {
    …
    exit;
}

$ergebnis = $db->query(…);
echo json_encode(…);
```
</details>

<details><summary>Tipp 2 – HTTP 500 / weiße Seite</summary>

Die Fehlermeldung steht im Log des Webservers: `tail /var/log/apache2/error.log`. „Access denied“ = Zugangsdaten falsch, „Table doesn't exist“ = Level 6 nicht ausgeführt, „syntax error“ = Tippfehler, oft ein fehlendes `;`.
</details>

> **Merke:** Eine Schnittstelle (API) gibt Daten in einem festen Format (JSON) heraus – und nur die Daten, die der Empfänger wirklich braucht.

**Denkfrage:** Für jede Tabelle und jede Aktion (lesen, anlegen, ändern, löschen) eine eigene PHP-Datei – wie viele Dateien wären das für 10 Tabellen? Was wäre besser? (→ Level 8)
