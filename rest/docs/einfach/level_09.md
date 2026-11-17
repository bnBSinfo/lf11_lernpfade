# Level 9 – Die REST-API aus Dart nutzen

**Ziel:** Ein eigenes Dart-Programm liest ToDos auf dem Pi. Es legt sie an, hakt sie ab und löscht sie. Genau so fragt später deine Flutter-App.

**Du schreibst:** ein neues Dart-Projekt `todo_client` auf dem PC

## Auftrag
1. **⌨️ Terminal (PC)** Lege ein neues Projekt an. Füge das Paket `http` hinzu:
   {{code 0}}
2. **📄 Neue Datei** `lib/todo_api.dart`. Darin stehen 2 Klassen:
   - **`ToDo`** mit `id` (int), `name` (String) und `checkbox` (bool). Dazu der Konstruktor **`ToDo.fromJson(Map<String, dynamic> json)`**. Achtung: `checkbox` kann `true`/`false` **oder** `1`/`0` sein.
   - **`TodoApi`**. Sie bekommt die IP. Daraus baut sie die Adresse `http://<IP>/php-crud-api/api.php/records/ToDoTB`. Sie hat 4 Methoden:

   | Methode | HTTP | gibt zurück |
   |---|---|---|
   | `Future<List<ToDo>> alle()` | `GET` | Liste aus `records` |
   | `Future<int> anlegen(String name)` | `POST` mit `{"name": …, "checkbox": false}` | neue id |
   | `Future<void> abhaken(int id, bool checkbox)` | `PUT` auf `…/ToDoTB/<id>` mit `{"checkbox": …}` | nichts |
   | `Future<void> loeschen(int id)` | `DELETE` auf `…/ToDoTB/<id>` | nichts |

   Jede Methode prüft den Statuscode. Ist er nicht 200? Dann wirft sie eine `Exception`.
3. **✏️ Ändern** Ersetze den Inhalt von `bin/todo_client.dart`. Das Programm geht so:
   {{code 1}}
   Nach jedem Befehl zeigt es die Liste. Zum Beispiel: `[x] 1: Pi einrichten`. Ist der Pi aus? Dann fängt es den Fehler mit `try`/`catch` ab. Es zeigt eine kurze Meldung.

## Profi-Auftrag
- Dart-Projekt `todo_client` mit dem Paket `http`.
- `lib/todo_api.dart`: Klasse `ToDo` und Klasse `TodoApi` mit `alle()`, `anlegen()`, `abhaken()`, `loeschen()`. Statuscode nicht 200: `Exception`.
- `bin/todo_client.dart`: Aufruf mit IP und Befehl (`neu`, `ab`, `weg`). Danach die Liste. Fehler als kurze Meldung.

## Erklärt – was passiert hier?

{{code 2}}

1. **`await`:** Die Antwort kommt über das Netz. Das dauert. Darum sind alle Methoden `async`. Sie geben ein `Future` zurück.
2. **Statuscode:** `200` heißt OK. Bei `404` oder `500` wirft dein Programm eine Exception.
3. **`jsonDecode`** macht aus JSON-Text Dart-Daten. `{}` wird eine `Map`. `[]` wird eine `List`.
4. **`map(...).toList()`** macht aus jedem JSON-Objekt ein `ToDo`.

Beim Senden ist es umgekehrt: `jsonEncode` macht aus einer Map JSON-Text. Der Header `Content-Type: application/json` sagt der API: Hier kommt JSON.

**Argumente:** `void main(List<String> args)` bekommt alles nach dem Dateinamen. `args[0]` ist die IP. `args[1]` ist der Befehl. `args[2]` ist der Wert.

<details><summary>Tipp 1 – Imports und Adresse</summary>

{{code 3}}
Im Hauptprogramm: `import 'package:todo_client/todo_api.dart';`
</details>

<details><summary>Tipp 2 – POST und PUT</summary>

{{code 4}}
`http.put(_eintrag(id), headers: …, body: …)` geht genauso. Auf POST antwortet die API nur mit einer Zahl: `jsonDecode(antwort.body) as int`.
</details>

<details><summary>Tipp 3 – fromJson</summary>

`checkbox: c == true || c == 1`. So passt beides.
</details>

<details><summary>Tipp 4 – „Connection refused“ oder Timeout</summary>

Stimmt die IP? Läuft der Pi? Öffne die Adresse im Browser. Geht es dort nicht? Dann liegt es nicht an deinem Dart-Code.
</details>

> **Merke:** HTTP-Anfragen brauchen `async` und `await`. `jsonDecode` liest JSON. `jsonEncode` schreibt JSON. Erst den Statuscode prüfen. Dann die Daten nutzen.

**Denkfrage:** In der Flutter-Einführung lag die ToDo-Liste in einer `Map` im State. Was ändert sich, wenn die Daten auf dem Pi liegen? Zum Beispiel bei 2 Handys?
