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
