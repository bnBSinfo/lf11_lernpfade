# Level 6 – Datenbank und Tabellen anlegen

**Ziel:** Auf dem Pi gibt es die Datenbank `flutterDB` mit einem eigenen Benutzer und den Tabellen für Login und ToDo-Liste der App.

**Sie schreiben:** `flutterdb.sql` auf dem Pi · **Skript:** SQL-Datenbank und User einrichten

## Auftrag
**📄 Neue Datei** `~/flutterdb.sql` – schreiben Sie auf dem Pi (per SSH, als root) ein SQL-Skript, das alles auf einmal anlegt:
```bash
cd ~
nano flutterdb.sql
```
Das Skript soll – in dieser Reihenfolge:

1. die Datenbank `flutterDB` löschen, falls es sie schon gibt (`DROP DATABASE IF EXISTS`), neu anlegen (Zeichensatz `utf8mb4`) und auswählen (`USE`),
2. den Benutzer `'flutterUser'@'localhost'` löschen, falls vorhanden, und mit dem Passwort `Pa$$w0rd` neu anlegen,
3. ihm **alle Rechte auf alle Tabellen** von flutterDB geben und die Rechte neu laden (`FLUSH PRIVILEGES`),
4. die Tabelle `flutterTB` anlegen und zwei Benutzer einfügen,
5. die Tabelle `ToDoTB` anlegen und zwei ToDos einfügen.

| Tabelle | Spalte | Typ und Eigenschaften |
|---|---|---|
| `flutterTB` | `id` | ganze Zahl, Primärschlüssel, zählt automatisch hoch |
| | `name` | Text bis 20 Zeichen, Pflichtfeld |
| | `passwordLogin` | Text bis 20 Zeichen, Pflichtfeld |
| `ToDoTB` | `id` | ganze Zahl, Primärschlüssel, zählt automatisch hoch |
| | `name` | Text bis 100 Zeichen, Pflichtfeld |
| | `checkbox` | wahr/falsch, Pflichtfeld, Standardwert falsch |

Daten: in `flutterTB` die Benutzer `berno` und `stoll` (Passwort jeweils `Pa$$w0rd`), in `ToDoTB` *Pi einrichten* (abgehakt) und *API testen* (offen).

Speichern (Strg+O, Enter), beenden (Strg+X) und ausführen:
```bash
mysql < flutterdb.sql
mysql -e "USE flutterDB; SHOW TABLES; SELECT * FROM ToDoTB;"
```

## Profi-Auftrag
- Ein Skript `~/flutterdb.sql`, das bei jedem Lauf alles sauber neu anlegt: Datenbank `flutterDB` (`utf8mb4`) und Benutzer `'flutterUser'@'localhost'` (`Pa$$w0rd`) mit allen Rechten – aber nur auf flutterDB.
- `flutterTB`: `id` (INT, AUTO_INCREMENT, PRIMARY KEY), `name` und `passwordLogin` (je bis 20 Zeichen, Pflicht) – Benutzer `berno` und `stoll`, Passwort jeweils `Pa$$w0rd`.
- `ToDoTB`: `id` wie oben, `name` (bis 100 Zeichen, Pflicht), `checkbox` (BOOLEAN, Pflicht, Standard falsch) – *Pi einrichten* (abgehakt) und *API testen* (offen).
- `mysql < flutterdb.sql` läuft fehlerfrei; `SHOW TABLES` zeigt beide Tabellen.

## Erklärt – was passiert hier?

```sql
CREATE USER 'flutterUser'@'localhost' IDENTIFIED BY 'Pa$$w0rd';
GRANT ALL PRIVILEGES ON flutterDB.* TO 'flutterUser'@'localhost';
```

- **Eigener Benutzer statt root:** PHP und REST-API melden sich mit `flutterUser` an. Der darf **nur** in `flutterDB` – wird das Passwort bekannt, sind die anderen Datenbanken sicher.
- `@'localhost'` – der Benutzer darf sich nur vom Pi selbst anmelden.
- `flutterDB.*` heißt *alle Tabellen in flutterDB*. Ohne `.*` meint MySQL eine **Tabelle** namens flutterDB.

```sql
id INT AUTO_INCREMENT PRIMARY KEY
```

- **PRIMARY KEY** – die id ist eindeutig, über sie findet man genau einen Datensatz. Die REST-API in Level 8 braucht das für Adressen wie `…/records/ToDoTB/3`.
- **AUTO_INCREMENT** – MySQL vergibt die nächste Nummer selbst. Deshalb steht die id beim `INSERT` nicht dabei.

Datentypen: `VARCHAR(100)` = Text bis 100 Zeichen, `BOOLEAN` = wahr/falsch (MySQL speichert 1/0), `NOT NULL` = Pflichtfeld, `DEFAULT FALSE` = Standardwert.

**Warum ein Skript statt einzelner Befehle?** Weil es mit `DROP … IF EXISTS` beginnt, können Sie es nach jeder Korrektur einfach erneut ausführen – die Datenbank entsteht jedes Mal sauber neu.

<details><summary>Tipp 1 – Anfang des Skripts</summary>

```sql
DROP DATABASE IF EXISTS flutterDB;
CREATE DATABASE flutterDB CHARACTER SET utf8mb4;
USE flutterDB;
```
</details>

<details><summary>Tipp 2 – Gerüst einer Tabelle</summary>

```sql
CREATE TABLE ToDoTB (
  id       … ,
  name     … ,
  checkbox …
);
INSERT INTO ToDoTB (name, checkbox) VALUES
  ('…', TRUE),
  ('…', FALSE);
```
Zwischen den Spalten steht ein Komma, nach der letzten nicht.
</details>

<details><summary>Tipp 3 – Fehler beim Ausführen</summary>

MySQL nennt die Zeile: `ERROR 1064 … at line 12`. Häufig: fehlendes Komma oder Semikolon, `"` statt `'`. Mit `nano +12 flutterdb.sql` springen Sie direkt in Zeile 12.
</details>

> **Merke:** Programme greifen mit einem eigenen Benutzer mit möglichst wenig Rechten auf die Datenbank zu. Jede Tabelle braucht einen Primärschlüssel.

**Denkfrage:** In `flutterTB` stehen die Passwörter im Klartext. Was passiert, wenn jemand die Tabelle ausliest? (→ Bonus)
