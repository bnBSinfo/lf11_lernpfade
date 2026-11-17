# Level 8 – Die fertige REST-API

**Ziel:** Mit der *php-crud-api* gibt es **alle** Tabellen über eine REST-Schnittstelle. Du kannst lesen, anlegen, ändern und löschen.

**Skript:** Schnittstelle zur Datenbank erstellen (php-crud-api)

## Auftrag
1. **⌨️ Terminal (Pi)** Lade die API auf den Pi. Sie ist nur 1 Datei: `api.php`.
   {{code 0}}
   **⬇ Download:** [api.php](downloads/api.php) (php-crud-api v2.16.7, MIT-Lizenz). Du kannst sie auch mit `scp` auf den Pi kopieren.
2. **✏️ Ändern** Öffne `api.php` ganz unten. Trag bei `$config` die Daten aus Level 6 ein. Lösche die roten Zeilen. Tippe die grünen ein:
   {{code 1}}
   {{code 2}}
3. **🌐 Browser** Teste im Browser:
   - `http://<IP>/php-crud-api/api.php/records/flutterTB`
   - `http://<IP>/php-crud-api/api.php/records/flutterTB/1`
   - `http://<IP>/php-crud-api/api.php/records/ToDoTB`
4. **⌨️ Terminal (PC)** Lege mit `curl` ein ToDo an. Hake es ab. Lösche es wieder. Die Befehle stehen in **📘 Wissen: REST**.

## Profi-Auftrag
- Die API liegt unter `/var/www/html/php-crud-api/`. Sie nutzt `flutterUser` und `flutterDB`.
- `…/records/flutterTB`, `…/records/flutterTB/1` und `…/records/ToDoTB` liefern JSON.
- Mit `curl` legst du ein ToDo an, hakst es ab und löschst es.

## Erklärt – was passiert hier?

**REST** heißt: Jede Tabelle hat eine **Adresse**. Die **HTTP-Methode** sagt, was passieren soll:

| Methode | Adresse | SQL dahinter | Antwort |
|---|---|---|---|
| `GET` | `/records/ToDoTB` | `SELECT * FROM ToDoTB` | `{"records":[…]}` |
| `GET` | `/records/ToDoTB/3` | `… WHERE id = 3` | `{"id":3,…}` |
| `POST` | `/records/ToDoTB` | `INSERT INTO ToDoTB …` | neue id, zum Beispiel `7` |
| `PUT` | `/records/ToDoTB/3` | `UPDATE … WHERE id = 3` | `1` |
| `DELETE` | `/records/ToDoTB/3` | `DELETE … WHERE id = 3` | `1` |

![JSON-Antwort im Browser](bilder/api_json.png)

Die API macht diese Adressen **selbst**. Für jede Tabelle. Ohne eigenes PHP. Einen Datensatz findet sie über den **Primärschlüssel**. Darum war `PRIMARY KEY` in Level 6 so wichtig.

<details><summary>Tipp 1 – {"code":1000,…} oder Access denied</summary>

Bei *Access denied* stimmen `username`, `password` oder `database` nicht. Vor den Zeilen darf kein `//` stehen.
</details>

<details><summary>Tipp 2 – Wie im Skript: git clone</summary>

{{code 3}}
Dann liegt das ganze Repository mit `.git`-Ordner auf dem Webserver. Das ist nicht gut (→ Bonus 5).
</details>

<details><summary>Tipp 3 – curl unter Windows</summary>

In der PowerShell ist `curl` etwas anderes. Nimm `curl.exe`. Oder nimm die SSH-Sitzung auf dem Pi mit `localhost` statt der IP.
</details>

> **Merke:** REST: Tabellen haben feste Adressen. GET liest, POST legt an, PUT ändert, DELETE löscht.

**Denkfrage:** Öffne `…/records/flutterTB`. Was siehst du, das dort nicht stehen sollte?
