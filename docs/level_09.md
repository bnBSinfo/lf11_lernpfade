# Level 9 – Die REST-API aus Dart nutzen

**Ziel:** Eine Dart-Klasse `TodoApi` liest, legt an, hakt ab und löscht ToDos auf dem Pi. Genau diese Klasse bindet Ihre Flutter-App später ein.

**Dateien:** `lib/todo_api.dart` · **Ausprobieren:** `dart run tool/todo_konsole.dart`

## Auftrag
Ergänzen Sie in `lib/todo_api.dart` die **TODOs 1–5**:
1. `ToDo.fromJson` – baut aus einem JSON-Objekt ein `ToDo`. `erledigt` kann `true`/`false` **oder** `1`/`0` sein.
2. `alle()` – `GET`, Antwort mit `jsonDecode` lesen, die Liste unter `records` in ToDos umwandeln.
3. `anlegen(titel)` – `POST` mit JSON-Body, gibt die neue id zurück.
4. `abhaken(id, erledigt)` – `PUT` auf den einzelnen Datensatz.
5. `loeschen(id)` – `DELETE` auf den einzelnen Datensatz.

Nach jedem TODO können Sie es ausprobieren:
```bash
dart run tool/todo_konsole.dart
dart run tool/todo_konsole.dart neu "Milch kaufen"
dart run tool/todo_konsole.dart ab 3
dart run tool/todo_konsole.dart weg 3
```

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
2. **Statuscode** – `200` heißt OK. Bei `404` oder `500` wirft `_pruefe` eine Exception mit der Meldung des Servers.
3. **`jsonDecode`** macht aus dem JSON-Text Dart-Objekte: `{}` → `Map`, `[]` → `List`.
4. **`map(...).toList()`** wandelt jedes JSON-Objekt in ein `ToDo` um.

Beim Senden ist es umgekehrt: `jsonEncode({'titel': titel, 'erledigt': false})` macht aus der Map JSON-Text. Der Header `Content-Type: application/json` sagt der API, wie sie den Body lesen soll.

## Prüfen
`dart run tool/pruefen.dart 9` – legt ein Prüf-ToDo an, hakt es ab und löscht es wieder.

<details><summary>Tipp 1 – fromJson</summary>

```dart
final e = json['erledigt'];
return ToDo(id: json['id'] as int, titel: json['titel'] as String, erledigt: e == true || e == 1);
```
</details>

<details><summary>Tipp 2 – POST und PUT</summary>

```dart
final antwort = await http.post(basis, headers: _json, body: jsonEncode({…}));
_pruefe(antwort);
return jsonDecode(antwort.body) as int;
```
`http.put(_eintrag(id), headers: _json, body: …)` funktioniert genauso.
</details>

<details><summary>Tipp 3 – „Connection refused“ / Timeout</summary>

Die IP kommt aus `pi.txt`. Läuft Ihr Pi? `dart run tool/pruefen.dart` zeigt, ab welchem Level es hakt.
</details>

> **Merke:** HTTP-Anfragen sind asynchron (`async`/`await`). JSON wird mit `jsonDecode` gelesen und mit `jsonEncode` geschrieben. Erst den Statuscode prüfen, dann die Daten verwenden.

**Denkfrage:** In der Flutter-Einführung lag die ToDo-Liste in einer `Map` im State. Was ändert sich, wenn die Daten jetzt auf dem Pi liegen – z. B. wenn zwei Handys dieselbe Liste benutzen?
