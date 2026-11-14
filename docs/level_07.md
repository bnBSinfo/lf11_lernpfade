# Level 7 – Löschen: Funktionen als Parameter

**Ziel:** Der Mülleimer sitzt im Stateless `ToDoItem`, die Liste aber im State von
`ToDoList`. Sie übergeben deshalb eine **Funktion** an das `ToDoItem`.

**Dateien:** `lib/level_07/todo_list.dart`, `lib/level_07/todo_item.dart` ·
**Skript:** Beispiel 2c

## Auftrag
1. `todo_list.dart`: `deleteItem(int i)` – in `setState` `todos.removeAt(i)`.
2. `todo_item.dart`: Feld `final VoidCallback remove;` und Konstruktor
   `const ToDoItem(this.title, this.remove, {super.key});`
3. `todo_item.dart`: Der `IconButton` bekommt `onPressed: () => remove()` (und das
   `const` davor muss weg).
4. `todo_list.dart`: im `itemBuilder` `ToDoItem(todos[i], () => deleteItem(i))`.

## Prüfen
`flutter test test/level_07_test.dart`

<details><summary>Tipp 1 – Was ist VoidCallback?</summary>

`VoidCallback` ist der Typ „Funktion ohne Parameter und ohne Rückgabe“. Er ist
genauer als `Function` (wie im Skript) – die IDE kann dann Fehler früher finden.
</details>

<details><summary>Tipp 2 – Rote Fehler nach Schritt 2</summary>

Nach der Konstruktor-Änderung meldet die IDE im `itemBuilder` einen Fehler: Dort fehlt
das zweite Argument. Genau das ist Schritt 4.
</details>

> **Merke:** Funktionen, die den State verändern, gehören in das Stateful Widget. Das
> Stateless Widget bekommt nur „einen Knopf“, mit dem es die Funktion auslösen kann.
