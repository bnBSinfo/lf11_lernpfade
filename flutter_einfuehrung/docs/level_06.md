# Level 6 – Die ToDo-Liste

**Ziel:** Ein Stateful Widget verwaltet eine Liste und erzeugt daraus `ToDoItem`s.
Neue Einträge kommen über einen Dialog hinzu.

**Sie schreiben:** `lib/todo_list.dart` neu, `lib/todo_app.dart` ändern · **Skript:** Beispiel 2b

## Auftrag
1. **📄 Neue Datei** `lib/todo_list.dart` mit dem **Stateful Widget** `ToDoList` (`stful` + Tab). Der Rahmen:
   ```diff
   + import 'package:flutter/material.dart';
   + import 'todo_item.dart';
   +
   + class ToDoList extends StatefulWidget {
   +   const ToDoList({super.key});
   +
   +   @override
   +   State<ToDoList> createState() => _ToDoListState();
   + }
   +
   + class _ToDoListState extends State<ToDoList> {
   +   List<String> todos = [];
   +
   +   void addItem(String item) {
   +     // Schritt 2
   +   }
   +
   +   void newEntry() {
   +     // Schritt 3
   +   }
   +
   +   @override
   +   Widget build(BuildContext context) {
   +     return Scaffold(
   +       // Schritt 4
   +     );
   +   }
   + }
   ```
2. **✏️ Ändern** `addItem(String item)`: in `setState` `todos.add(item)`, danach (außerhalb von `setState`)
   `Navigator.of(context).pop();` – das schließt den Dialog. Der Kommentar `// Schritt 2` fliegt raus:
   ```diff
     void addItem(String item) {
   -   // Schritt 2
   +   setState(() {
   +     todos.add(item);
   +   });
   +   Navigator.of(context).pop();
     }
   ```
3. **✏️ Ändern** `newEntry()`: `showDialog` mit einem `AlertDialog`, dessen `content` ein
   `TextField(onSubmitted: addItem)` ist:
   ```diff
     void newEntry() {
   -   // Schritt 3
   +   showDialog<AlertDialog>(
   +     context: context,
   +     builder: (BuildContext context) {
   +       return AlertDialog(
   +         content: TextField(
   +           autofocus: true,
   +           onSubmitted: addItem,
   +         ),
   +       );
   +     },
   +   );
     }
   ```
4. **✏️ Ändern** Im `Scaffold` (statt des Kommentars) `appBar`, `body` mit dem `ListView.builder` und
   `floatingActionButton`. Der `ListView.builder` baut für jeden Index `i` ein `ToDoItem(todos[i])`:
   ```diff
       return Scaffold(
   -     // Schritt 4
   +     appBar: AppBar(title: const Text('ToDo Liste')),
   +     body: ListView.builder(
   +       itemCount: todos.length,
   +       itemBuilder: (context, i) {
   +         return ToDoItem(todos[i]);
   +       },
   +     ),
   +     floatingActionButton: FloatingActionButton(
   +       onPressed: newEntry,
   +       child: const Icon(Icons.add),
   +     ),
       );
   ```
5. **✏️ Ändern** `lib/todo_app.dart` – die Vorschau aus Level 5 hat ausgedient. Import und den **ganzen**
   Inhalt von `build` **ersetzen**:
   ```diff
     import 'package:flutter/material.dart';
   - import 'todo_item.dart';
   + import 'todo_list.dart';
     …
     Widget build(BuildContext context) {
   -   return MaterialApp(
   -     home: Scaffold(
   -       … (die ganze Vorschau mit den drei ToDoItems)
   -     ),
   -   );
   +   return const MaterialApp(home: ToDoList());
     }
   ```

## Profi-Auftrag
- `lib/todo_list.dart`: Stateful Widget `ToDoList`, die Titel liegen als Liste im State.
- AppBar „ToDo Liste“, darunter ein `ToDoItem` je Eintrag (`ListView.builder`), unten rechts ein Plus-Button.
- Plus öffnet einen `AlertDialog` mit Textfeld; Enter fügt den Eintrag hinzu und schließt den Dialog.
- `ToDoApp` startet direkt die `ToDoList`.

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

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
