# Level 8 – Abhaken: von der List zur Map

**Ziel:** Zu jedem Titel gehört jetzt ein zweiter Wert (abgehakt ja/nein). Dafür
wandeln Sie die Liste in eine `Map<String, bool>` um.

**Sie ändern:** `lib/todo_list.dart`, `lib/todo_item.dart` ·
**Skript:** Beispiel 2d

## Auftrag
Gehen Sie in der Reihenfolge 1 → 6 vor. Nach Schritt 1 sind alle Stellen rot unterstrichen, die noch mit der
Liste arbeiten – genau die ändern Sie in den Schritten danach.

1. **✏️ Ändern** `lib/todo_list.dart` – die Liste durch eine Map **ersetzen**:
   ```diff
     class _ToDoListState extends State<ToDoList> {
   -   List<String> todos = [];
   +   Map<String, bool> todos = {};
   ```
2. **✏️ Ändern** `lib/todo_list.dart` – `addItem` und `deleteItem` arbeiten jetzt mit der Map:
   ```diff
     void addItem(String item) {
       setState(() {
   -     todos.add(item);
   +     todos[item] = false;
       });
       Navigator.of(context).pop();
     }

   - void deleteItem(int i) {
   + void deleteItem(String key) {
       setState(() {
   -     todos.removeAt(i);
   +     todos.remove(key);
       });
     }
   ```
3. **✏️ Ändern** `lib/todo_list.dart` – neue Methode `checkBoxDone` direkt **unter** `deleteItem` einfügen:
   ```diff
   + void checkBoxDone(String key) {
   +   setState(() {
   +     todos.update(key, (bool done) => !done);
   +   });
   + }
   ```
4. **✏️ Ändern** `lib/todo_item.dart` – zwei Felder **hinzufügen**, Konstruktor **ersetzen**:
   ```diff
       final String title;
   +   final bool done;
       final VoidCallback remove;
   +   final VoidCallback checkBoxDone;

   -   const ToDoItem(this.title, this.remove, {super.key});
   +   const ToDoItem(this.title, this.done, this.remove, this.checkBoxDone,
   +       {super.key});
   ```
5. **✏️ Ändern** `lib/todo_item.dart` – die Checkbox wird aktiv (das `const` muss weg):
   ```diff
         children: [
   -       const Checkbox(value: false, onChanged: null),
   +       Checkbox(
   +         value: done,
   +         onChanged: (value) => checkBoxDone(),
   +       ),
           Expanded(child: Text(title)),
   ```
6. **✏️ Ändern** `lib/todo_list.dart` – im `itemBuilder` die eine `return`-Zeile **ersetzen**:
   ```diff
           itemBuilder: (context, i) {
   -         return ToDoItem(todos[i], () => deleteItem(i));
   +         var key = todos.keys.elementAt(i);
   +         return ToDoItem(
   +           key, // Titel
   +           todos.values.elementAt(i), // Checkboxstatus
   +           () => deleteItem(key), // Löschfunktion
   +           () => checkBoxDone(key), // Checkboxfunktion
   +         );
           },
   ```

## Profi-Auftrag
- Jedes ToDo hat einen Erledigt-Status. Die Checkbox zeigt ihn und schaltet ihn beim Antippen um.
- Die Daten liegen als `Map<String, bool>` vor (Titel → erledigt).
- `ToDoItem(title, done, remove, checkBoxDone)` – weiterhin Stateless.
- Hinzufügen und Löschen funktionieren weiter.

*Hängen Sie fest? Schalten Sie oben auf **🧭 Begleitet** um – dort steht jeder Schritt mit Code-Rahmen.*

## Erklärt – was passiert hier?

**Warum eine Map?** Zu jedem ToDo gehören jetzt **zwei** Informationen: Titel und Haken. Eine `List<String>` kann pro Platz nur einen Wert speichern. Eine `Map<String, bool>` ordnet jedem **Schlüssel** (Titel) einen **Wert** (abgehakt ja/nein) zu:

```dart
Map<String, bool> todos = {
  'Milch kaufen': true,
  'LF11 lernen': false,
};
```

| Aufgabe | List | Map |
|---|---|---|
| hinzufügen | `todos.add('Milch')` | `todos['Milch'] = false` |
| löschen | `todos.removeAt(i)` | `todos.remove('Milch')` |
| Anzahl | `todos.length` | `todos.length` |
| i-tes Element | `todos[i]` | `todos.keys.elementAt(i)` (Schlüssel) und `todos.values.elementAt(i)` (Wert) |

**Der Haken – wieder über eine Funktion:** Die Checkbox sitzt im Stateless `ToDoItem`, die Daten im State der Liste. Also gleiches Muster wie beim Löschen:

1. Checkbox antippen → `onChanged: (value) => checkBoxDone()`.
2. `checkBoxDone` ist `() => checkBoxDone(key)` aus der Liste.
3. `todos.update(key, (bool done) => !done)` dreht den Wert um: `false` → `true` → `false`.
4. `setState` → `build` → das `ToDoItem` bekommt den neuen Wert als `done` und zeigt den Haken.

**Beachten Sie:** `ToDoItem` bleibt **Stateless** – es merkt sich den Haken nicht selbst, sondern bekommt ihn bei jedem Neuzeichnen von außen (`done`). Nur so passen Anzeige und Daten immer zusammen.

<details><summary>Tipp – Viele rote Fehler auf einmal?</summary>

Gehen Sie in der Reihenfolge 1 → 6 vor. Nach Schritt 1 sind alle Stellen rot, die
noch mit der Liste arbeiten – sie zeigen Ihnen genau, was Sie anpassen müssen.
</details>

**Denkfrage:** Was passiert, wenn Sie zweimal „Einkaufen“ eintragen? Warum?
(→ `docs/bonus.md`)
