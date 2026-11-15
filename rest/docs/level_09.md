# Level 9 – Die REST-API aus Dart nutzen

**Ziel:** Ein eigenes Dart-Programm liest, legt an, hakt ab und löscht ToDos auf dem Pi. Dieselben Anfragen schickt später Ihre Flutter-App (Lernpfad Flutter-Datenbankanbindung).

**Sie schreiben:** ein neues Dart-Projekt `todo_client` auf dem PC

## Auftrag
1. Legen Sie auf dem PC ein neues Projekt an und fügen Sie das Paket `http` hinzu:
   ```bash
   dart create todo_client
   cd todo_client
   dart pub add http
   ```
2. Legen Sie die Datei `lib/todo_api.dart` an. Sie enthält:
   - eine Klasse **`ToDo`** mit den Feldern `id` (int), `name` (String), `checkbox` (bool) und einem Konstruktor **`ToDo.fromJson(Map<String, dynamic> json)`**. Achtung: `checkbox` kann je nach Server `true`/`false` **oder** `1`/`0` sein.
   - eine Klasse **`TodoApi`**, die im Konstruktor die IP bekommt und daraus die Adresse `http://<IP>/php-crud-api/api.php/records/ToDoTB` baut, mit den Methoden:

   | Methode | HTTP | Rückgabe |
   |---|---|---|
   | `Future<List<ToDo>> alle()` | `GET` auf die Tabelle | Liste aus `records` |
   | `Future<int> anlegen(String name)` | `POST` auf die Tabelle, Body `{"name": …, "checkbox": false}` | neue id |
   | `Future<void> abhaken(int id, bool checkbox)` | `PUT` auf `…/ToDoTB/<id>`, Body `{"checkbox": …}` | – |
   | `Future<void> loeschen(int id)` | `DELETE` auf `…/ToDoTB/<id>` | – |

   Jede Methode prüft den Statuscode und wirft bei allem außer 200 eine `Exception` mit Code und Antworttext.
3. Ersetzen Sie den Inhalt von `bin/todo_client.dart` durch ein Hauptprogramm, das so aufgerufen wird:
   ```bash
   dart run bin/todo_client.dart 10.36.13.76                      # alle ToDos anzeigen
   dart run bin/todo_client.dart 10.36.13.76 neu "Milch kaufen"
   dart run bin/todo_client.dart 10.36.13.76 ab 3                 # ToDo 3 abhaken
   dart run bin/todo_client.dart 10.36.13.76 weg 3                # ToDo 3 löschen
   ```
   Nach jedem Befehl zeigt es die Liste an, z. B. `[x] 1: Pi einrichten`. Fehler (z. B. Pi aus) fängt es mit `try`/`catch` ab und gibt eine kurze Meldung aus.

## Erklärt – was passiert hier?

```dart
final antwort = await http.get(basis);            // ① Anfrage an den Pi, warten
_pruefe(antwort);                                 // ② Statuscode 200?
final daten = jsonDecode(antwort.body)            // ③ Text → Map
    as Map<String, dynamic>;
return (daten['records'] as List)                 // ④ Liste unter "records"
    .map((r) => ToDo.fromJson(r as Map<String, dynamic>))
    .toList();
```

1. **`await`** – die Antwort kommt über das Netz, das dauert. Deshalb sind alle Methoden `async` und geben ein `Future` zurück.
2. **Statuscode** – `200` heißt OK. Bei `404` oder `500` soll Ihr Programm eine Exception mit der Meldung des Servers werfen.
3. **`jsonDecode`** (aus `dart:convert`) macht aus dem JSON-Text Dart-Objekte: `{}` → `Map`, `[]` → `List`.
4. **`map(...).toList()`** wandelt jedes JSON-Objekt in ein `ToDo` um.

Beim Senden ist es umgekehrt: `jsonEncode({'name': name, 'checkbox': false})` macht aus der Map JSON-Text. Der Header `Content-Type: application/json` sagt der API, wie sie den Body lesen soll.

**Kommandozeilen-Argumente:** `void main(List<String> args)` bekommt alles hinter dem Dateinamen als Liste: `args[0]` ist die IP, `args[1]` der Befehl, `args[2]` der Wert.

<details><summary>Tipp 1 – Imports und Adresse</summary>

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class TodoApi {
  TodoApi(String ip) : basis = Uri.parse('http://$ip/php-crud-api/api.php/records/ToDoTB');
  final Uri basis;
  Uri _eintrag(int id) => Uri.parse('$basis/$id');
  …
}
```
Im Hauptprogramm: `import 'package:todo_client/todo_api.dart';`
</details>

<details><summary>Tipp 2 – POST und PUT</summary>

```dart
final antwort = await http.post(basis,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({…}));
```
`http.put(_eintrag(id), headers: …, body: …)` funktioniert genauso. Die Antwort auf POST ist nur eine Zahl: `jsonDecode(antwort.body) as int`.
</details>

<details><summary>Tipp 3 – fromJson</summary>

`checkbox: c == true || c == 1` – so ist beides abgedeckt.
</details>

<details><summary>Tipp 4 – „Connection refused“ / Timeout</summary>

Stimmt die IP? Läuft der Pi? Öffnen Sie dieselbe Adresse im Browser – klappt es dort nicht, liegt es nicht an Ihrem Dart-Code.
</details>

> **Merke:** HTTP-Anfragen sind asynchron (`async`/`await`). JSON wird mit `jsonDecode` gelesen und mit `jsonEncode` geschrieben. Erst den Statuscode prüfen, dann die Daten verwenden.

**Denkfrage:** In der Flutter-Einführung lag die ToDo-Liste in einer `Map` im State. Was ändert sich, wenn die Daten jetzt auf dem Pi liegen – z. B. wenn zwei Handys dieselbe Liste benutzen?
