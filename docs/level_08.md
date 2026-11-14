# Level 8 – Abhaken: von der List zur Map

**Ziel:** Zu jedem Titel gehört jetzt ein zweiter Wert (abgehakt ja/nein). Dafür
wandeln Sie die Liste in eine `Map<String, bool>` um.

**Dateien:** `lib/level_08/todo_list.dart`, `lib/level_08/todo_item.dart` ·
**Skript:** Beispiel 2d

## Auftrag
1. `Map<String, bool> todos = {};` statt der Liste.
2. `addItem`: `todos[item] = false;` · `deleteItem(String key)`: `todos.remove(key);`
3. Neu: `checkBoxDone(String key)` – in `setState`
   `todos.update(key, (bool done) => !done);`
4. `todo_item.dart`: Felder `final bool done;` und `final VoidCallback checkBoxDone;`,
   Konstruktor `(this.title, this.done, this.remove, this.checkBoxDone, {super.key})`.
5. Die Checkbox: `value: done`, `onChanged: (value) => checkBoxDone()`.
6. `itemBuilder`:
   ```dart
   var key = todos.keys.elementAt(i);
   return ToDoItem(
     key,                         // Titel
     todos.values.elementAt(i),   // Checkboxstatus
     () => deleteItem(key),       // Löschfunktion
     () => checkBoxDone(key),     // Checkboxfunktion
   );
   ```

## Prüfen
`flutter test test/level_08_test.dart` – und dann `dart run tool/fortschritt.dart` 🎉

<details><summary>Tipp – Viele rote Fehler auf einmal?</summary>

Gehen Sie in der Reihenfolge 1 → 6 vor. Nach Schritt 1 sind alle Stellen rot, die
noch mit der Liste arbeiten – sie zeigen Ihnen genau, was Sie anpassen müssen.
</details>

**Denkfrage:** Was passiert, wenn Sie zweimal „Einkaufen“ eintragen? Warum?
(→ `docs/bonus.md`)
