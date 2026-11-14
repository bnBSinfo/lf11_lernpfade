# Level 6 – Datenbank und Tabellen anlegen

**Ziel:** Auf dem Pi gibt es die Datenbank `flutterDB` mit einem eigenen Benutzer und den Tabellen für Login und ToDo-Liste der App.

**Dateien:** `server/sql/flutterdb.sql` · **Skript:** SQL-Datenbank und User einrichten

## Auftrag
1. Ergänzen Sie auf dem PC in `server/sql/flutterdb.sql` die **TODOs 1–5**.
2. Prüfen Sie die Datei: `dart run tool/pruefen.dart 6`
3. Kopieren Sie die Datei auf den Pi und führen Sie sie aus:
   ```bash
   scp server/sql/flutterdb.sql administrator@<IP>:/tmp/      # auf dem PC
   mysql < /tmp/flutterdb.sql                                # auf dem Pi (als root)
   ```
4. Melden Sie sich in phpMyAdmin als `flutterUser` an und sehen Sie sich beide Tabellen an.

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

Datentypen für ToDoTB: `VARCHAR(100)` = Text bis 100 Zeichen, `BOOLEAN` = wahr/falsch (MySQL speichert 1/0), `NOT NULL` = Pflichtfeld, `DEFAULT FALSE` = Standardwert.

## Prüfen
`dart run tool/pruefen.dart 6` prüft Ihre SQL-Datei. Ob sie auf dem Pi richtig ausgeführt wurde, zeigt Level 7.

<details><summary>Tipp 1 – TODO 3</summary>

Die Spalte gehört als erste Zeile in die Klammer, mit Komma danach:
```sql
CREATE TABLE flutterTB (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name …
```
</details>

<details><summary>Tipp 2 – TODO 4 Gerüst</summary>

```sql
CREATE TABLE ToDoTB (
  id       … ,
  titel    … ,
  erledigt …
);
```
</details>

<details><summary>Tipp 3 – Fehler beim Ausführen</summary>

MySQL nennt die Zeile: `ERROR 1064 … at line 12`. Häufig: fehlendes Komma oder Semikolon. Die Datei beginnt mit `DROP DATABASE IF EXISTS` – Sie können sie also nach jeder Korrektur einfach erneut ausführen.
</details>

> **Merke:** Programme greifen mit einem eigenen Benutzer mit möglichst wenig Rechten auf die Datenbank zu. Jede Tabelle braucht einen Primärschlüssel.

**Denkfrage:** In `flutterTB` stehen die Passwörter im Klartext. Was passiert, wenn jemand die Tabelle ausliest? (→ Bonus)
