# Level 7 – Löschen: Funktionen als Parameter

**Ziel:** Der Mülleimer sitzt im Stateless `ToDoItem`, die Liste aber im State von
`ToDoList`. Sie übergeben deshalb eine **Funktion** an das `ToDoItem`.

**Sie ändern:** `lib/todo_list.dart`, `lib/todo_item.dart` ·
**Skript:** Beispiel 2c

## Auftrag
1. **✏️ Ändern** `lib/todo_list.dart` – eine neue Methode `deleteItem` **zwischen** `addItem` und `newEntry` einfügen:
   ```diff
     void addItem(String item) {
       …
     }

   + void deleteItem(int i) {
   +   setState(() {
   +     todos.removeAt(i);
   +   });
   + }
   +
     void newEntry() {
   ```
2. **✏️ Ändern** `lib/todo_item.dart` – ein neues Feld **hinzufügen** und den Konstruktor **ersetzen**:
   ```diff
     class ToDoItem extends StatelessWidget {
       final String title;
   +   final VoidCallback remove;

   -   const ToDoItem(this.title, {super.key});
   +   const ToDoItem(this.title, this.remove, {super.key});
   ```
3. **✏️ Ändern** `lib/todo_item.dart` – der `IconButton` wird aktiv. Das `const` muss weg, weil `remove` erst zur
   Laufzeit feststeht:
   ```diff
           Expanded(child: Text(title)),
   -       const IconButton(
   -         icon: Icon(Icons.delete),
   -         onPressed: null,
   -       ),
   +       IconButton(
   +         icon: const Icon(Icons.delete),
   +         onPressed: () => remove(),
   +       ),
   ```
4. **✏️ Ändern** `lib/todo_list.dart` – im `itemBuilder` bekommt jedes `ToDoItem` seine Löschfunktion:
   ```diff
           itemBuilder: (context, i) {
   -         return ToDoItem(todos[i]);
   +         return ToDoItem(todos[i], () => deleteItem(i));
           },
   ```

## Profi-Auftrag
- Der Mülleimer löscht **genau sein** ToDo.
- `ToDoItem` bleibt **Stateless**: Gelöscht wird im State der Liste. Die Löschfunktion bekommt das Item als zweiten
  Konstruktor-Parameter (`VoidCallback`).

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

## Erklärt – was passiert hier?

**Das Problem:** Der Mülleimer sitzt im `ToDoItem`. Die Liste `todos` liegt aber im State von `ToDoList`. Ein Stateless Widget hat kein `setState` und kennt die Liste nicht – es kann also nicht selbst löschen.

**Die Lösung: Die Liste gibt dem Eintrag eine Funktion mit** – wie eine Fernbedienung:

```dart
// in ToDoList (Stateful) – hier wird wirklich gelöscht
void deleteItem(int i) {
  setState(() { todos.removeAt(i); });
}
// beim Bauen jedes Eintrags:
ToDoItem(todos[i], () => deleteItem(i))
```

```dart
// in ToDoItem (Stateless) – kennt nur die „Fernbedienung“
final VoidCallback remove;
IconButton(onPressed: () => remove(), icon: const Icon(Icons.delete))
```

**Was passiert beim Tippen auf den Mülleimer von „LF11 lernen“ (Index 1)?**

1. `IconButton` ruft `remove()` auf.
2. `remove` ist die Funktion `() => deleteItem(1)`, die die Liste beim Bauen übergeben hat.
3. `deleteItem(1)` entfernt in `setState` den Eintrag an Position 1.
4. `build` von `ToDoList` läuft neu → `ListView.builder` baut nur noch die übrigen Einträge.

**`() => deleteItem(i)`** ist eine **anonyme Funktion** (ohne Namen). Sie wird nicht sofort ausgeführt, sondern erst, wenn jemand `remove()` aufruft. Jeder Eintrag bekommt seine eigene Funktion mit seinem eigenen `i`.

**`VoidCallback`** ist der Typ „Funktion ohne Parameter, ohne Rückgabe“ – genauer als `Function`.

> Dieses Muster heißt **„State nach oben heben“**: Daten liegen im gemeinsamen Eltern-Widget, Kinder melden Ereignisse über Funktionen nach oben.

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
