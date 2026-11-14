# Level 6 – Die ToDo-Liste

**Ziel:** Ein Stateful Widget verwaltet eine Liste und erzeugt daraus `ToDoItem`s.
Neue Einträge kommen über einen Dialog hinzu.

**Datei:** `lib/level_06/todo_list.dart` · **Skript:** Beispiel 2b · Ansehen: `aktivesLevel = 6`

## Auftrag
1. `List<String> todos = [];`
2. `addItem(String item)`: in `setState` `todos.add(item)`, danach
   `Navigator.of(context).pop();` (schließt den Dialog).
3. `newEntry()`: `showDialog` mit einem `AlertDialog`, dessen `content` ein
   `TextField(onSubmitted: addItem)` ist.
4. `build`: `Scaffold` mit
   - `appBar: AppBar(title: Text('ToDo Liste'))`
   - `body: ListView.builder(itemCount: todos.length, itemBuilder: …)` – baut für
     jeden Index `i` ein `ToDoItem(todos[i])`
   - `floatingActionButton: FloatingActionButton(onPressed: newEntry, child: Icon(Icons.add))`

## Erklärt – was passiert hier?

**Warum ist `ToDoList` Stateful?** Die Liste **ändert sich**, während die App läuft: Einträge kommen hinzu. Also braucht sie einen State mit der Variable `todos`.

**`ListView.builder` – eine Liste aus Daten bauen:**

```dart
ListView.builder(
  itemCount: todos.length,          // so viele Einträge gibt es
  itemBuilder: (context, i) {       // wird für jeden Index i aufgerufen
    return ToDoItem(todos[i]);      // aus Daten wird ein Widget
  },
)
```

Sie schreiben **nicht** jedes `ToDoItem` von Hand. Sie sagen nur, **wie viele** es gibt und **wie man eins baut**. Hat `todos` zwei Einträge, ruft Flutter `itemBuilder` mit `i = 0` und `i = 1` auf.

**Der Dialog Schritt für Schritt:**

1. Tippen auf `+` → `onPressed: newEntry` ruft `newEntry()` auf.
2. `showDialog(...)` legt einen `AlertDialog` über die Seite. `builder:` sagt, wie der Dialog aussieht.
3. Enter im TextField → `onSubmitted: addItem` ruft `addItem('Milch kaufen')` auf.
4. `addItem` fügt in `setState` den Text zu `todos` hinzu → `build` läuft neu → die Liste hat einen Eintrag mehr.
5. `Navigator.of(context).pop()` schließt den Dialog wieder. Ein Dialog ist für Flutter wie eine kleine neue Seite – `pop` nimmt die oberste Seite weg.

**Hier arbeiten Stateful und Stateless zusammen:** `ToDoList` (Stateful) besitzt die Daten, `ToDoItem` (Stateless) zeigt einen Eintrag davon an.

## Prüfen
`flutter test test/level_06_test.dart`

<details><summary>Tipp 1 – showDialog</summary>

```dart
void newEntry() {
  showDialog<AlertDialog>(
    context: context,
    builder: (BuildContext context) {
      return AlertDialog(
        content: TextField(autofocus: true, onSubmitted: addItem),
      );
    },
  );
}
```
</details>

<details><summary>Tipp 2 – ListView.builder</summary>

```dart
ListView.builder(
  itemCount: todos.length,
  itemBuilder: (context, i) {
    return ToDoItem(todos[i]);
  },
),
```
</details>

> **Merke:** `onPressed: newEntry` übergibt die **Methode selbst** (ohne Klammern).
> Mit Klammern `newEntry()` würde sie sofort beim Bauen ausgeführt.

**Achtung Skript:** Dort heißt die Liste an einer Stelle `products` – verwenden Sie
überall `todos`.
