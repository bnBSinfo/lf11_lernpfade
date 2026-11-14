# Level 8 – Die fertige REST-API

**Ziel:** Mit der *php-crud-api* stellen Sie **alle** Tabellen über eine einheitliche REST-Schnittstelle bereit – lesen, anlegen, ändern und löschen.

**Skript:** Schnittstelle zur Datenbank erstellen (php-crud-api)

## Auftrag
1. Laden Sie die API in das Webverzeichnis:
   ```bash
   apt install -y git
   cd /var/www/html
   git clone https://github.com/mevdschee/php-crud-api.git
   ```
2. Tragen Sie in `php-crud-api/api.php` ganz unten bei `$config` die Zugangsdaten aus Level 6 ein:
   ```bash
   nano +99999 /var/www/html/php-crud-api/api.php
   ```
   ![Zugangsdaten in api.php](bilder/api_config.png)
3. Testen Sie im Browser:
   - `http://<IP>/php-crud-api/api.php/records/flutterTB`
   - `http://<IP>/php-crud-api/api.php/records/flutterTB/1`
   - `http://<IP>/php-crud-api/api.php/records/ToDoTB`
4. Legen Sie vom PC aus mit `curl` ein ToDo an, haken Sie es ab und löschen Sie es wieder (siehe **📘 Wissen: REST**).

## Erklärt – was passiert hier?

**REST** heißt: Jede Tabelle ist eine **Ressource** mit einer Adresse, die **HTTP-Methode** sagt, was passieren soll:

| Methode | Adresse | SQL dahinter | Antwort |
|---|---|---|---|
| `GET` | `/records/ToDoTB` | `SELECT * FROM ToDoTB` | `{"records":[…]}` |
| `GET` | `/records/ToDoTB/3` | `… WHERE id = 3` | `{"id":3,…}` |
| `POST` | `/records/ToDoTB` | `INSERT INTO ToDoTB …` | neue id, z. B. `7` |
| `PUT` | `/records/ToDoTB/3` | `UPDATE ToDoTB SET … WHERE id = 3` | `1` (geänderte Zeilen) |
| `DELETE` | `/records/ToDoTB/3` | `DELETE FROM ToDoTB WHERE id = 3` | `1` |

![JSON-Antwort im Browser](bilder/api_json.png)

Die API liest beim Start die Tabellen aus der Datenbank und erzeugt diese Adressen **automatisch** – für jede Tabelle, ohne eine Zeile eigenes PHP. Einzelne Datensätze findet sie über den **Primärschlüssel** – deshalb war TODO 3 in Level 6 so wichtig.

## Prüfen
`dart run tool/pruefen.dart 8`

<details><summary>Tipp 1 – {"code":1000,…} oder Access denied</summary>

Die API meldet Fehler als JSON mit `code` und `message`. Bei *Access denied* stimmen `username`, `password` oder `database` in `$config` nicht. Die Zeilen dürfen nicht mit `//` auskommentiert sein.
</details>

<details><summary>Tipp 2 – curl unter Windows</summary>

In der PowerShell heißt `curl` etwas anderes. Nehmen Sie `curl.exe` – oder die SSH-Sitzung auf dem Pi mit `localhost` statt der IP.
</details>

> **Merke:** REST = Ressourcen (Tabellen) unter festen Adressen + HTTP-Methoden GET, POST, PUT, DELETE für Lesen, Anlegen, Ändern, Löschen (CRUD).

**Denkfrage:** Rufen Sie `…/records/flutterTB` auf. Was sehen Sie, das dort nicht stehen sollte? Vergleichen Sie mit Ihrer Schnittstelle aus Level 7. (→ Bonus)
