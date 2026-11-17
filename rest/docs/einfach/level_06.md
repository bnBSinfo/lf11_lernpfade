# Level 6 – Datenbank und Tabellen anlegen

**Ziel:** Auf dem Pi gibt es die Datenbank `flutterDB`. Sie hat einen eigenen Benutzer. Sie hat die Tabellen für Login und ToDo-Liste.

**Du schreibst:** `flutterdb.sql` auf dem Pi · **Skript:** SQL-Datenbank und User einrichten

## Auftrag
**📄 Neue Datei** `~/flutterdb.sql`. Schreib auf dem Pi ein SQL-Skript. Es legt alles auf einmal an:
{{code 0}}
Das Skript macht diese 5 Dinge. Halte die Reihenfolge ein:

1. Lösche die Datenbank `flutterDB`, falls es sie gibt (`DROP DATABASE IF EXISTS`). Lege sie neu an (Zeichensatz `utf8mb4`). Wähle sie aus (`USE`).
2. Lösche den Benutzer `'flutterUser'@'localhost'`, falls es ihn gibt. Lege ihn neu an. Passwort: `Pa$$w0rd`.
3. Gib ihm **alle Rechte auf alle Tabellen** in flutterDB. Lade dann die Rechte neu (`FLUSH PRIVILEGES`).
4. Lege die Tabelle `flutterTB` an. Füge 2 Benutzer ein.
5. Lege die Tabelle `ToDoTB` an. Füge 2 ToDos ein.

| Tabelle | Spalte | Typ |
|---|---|---|
| `flutterTB` | `id` | ganze Zahl, Primärschlüssel, zählt selbst hoch |
| | `name` | Text bis 20 Zeichen, muss da sein |
| | `passwordLogin` | Text bis 20 Zeichen, muss da sein |
| `ToDoTB` | `id` | ganze Zahl, Primärschlüssel, zählt selbst hoch |
| | `name` | Text bis 100 Zeichen, muss da sein |
| | `checkbox` | wahr oder falsch, muss da sein, am Anfang falsch |

Daten: in `flutterTB` die Benutzer `berno` und `stoll`. Beide haben das Passwort `Pa$$w0rd`. In `ToDoTB`: *Pi einrichten* (abgehakt) und *API testen* (offen).

Speichern: Strg+O, Enter. Beenden: Strg+X. Dann ausführen:
{{code 1}}

## Profi-Auftrag
- `~/flutterdb.sql` legt bei jedem Lauf alles neu an: `flutterDB` und `flutterUser` mit Rechten nur auf flutterDB.
- `flutterTB`: `id`, `name`, `passwordLogin`. Benutzer `berno` und `stoll`.
- `ToDoTB`: `id`, `name`, `checkbox`. *Pi einrichten* (abgehakt) und *API testen* (offen).
- `mysql < flutterdb.sql` läuft ohne Fehler.

## Erklärt – was passiert hier?

{{code 2}}

- **Eigener Benutzer statt root:** PHP und die API melden sich als `flutterUser` an. Er darf **nur** in `flutterDB`. Kennt jemand sein Passwort, sind die anderen Datenbanken trotzdem sicher.
- `@'localhost'` heißt: Er darf nur vom Pi selbst rein.
- `flutterDB.*` heißt: alle Tabellen in flutterDB.

{{code 3}}

- **PRIMARY KEY:** Die id gibt es nur 1-mal. Damit findest du genau 1 Datensatz. Die API in Level 8 braucht das.
- **AUTO_INCREMENT:** MySQL zählt die id selbst hoch. Darum fehlt die id beim `INSERT`.

`VARCHAR(100)` heißt: Text bis 100 Zeichen. `BOOLEAN` heißt: wahr oder falsch. `NOT NULL` heißt: muss da sein.

**Warum ein Skript?** Es beginnt mit `DROP … IF EXISTS`. Darum kannst du es nach jedem Fehler einfach neu starten.

<details><summary>Tipp 1 – Anfang vom Skript</summary>

{{code 4}}
</details>

<details><summary>Tipp 2 – Gerüst für eine Tabelle</summary>

{{code 5}}
Zwischen den Spalten steht ein Komma. Nach der letzten nicht.
</details>

<details><summary>Tipp 3 – Fehler beim Ausführen</summary>

MySQL nennt die Zeile. Zum Beispiel: `ERROR 1064 … at line 12`. Oft fehlt ein Komma oder ein Semikolon. Mit `nano +12 flutterdb.sql` springst du in Zeile 12.
</details>

> **Merke:** Programme nutzen einen eigenen Benutzer mit wenig Rechten. Jede Tabelle braucht einen Primärschlüssel.

**Denkfrage:** In `flutterTB` stehen die Passwörter im Klartext. Was passiert, wenn jemand die Tabelle liest?
