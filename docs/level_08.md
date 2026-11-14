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

## Prüfen
`flutter test test/level_08_test.dart` – und dann `dart run tool/fortschritt.dart` 🎉

<details><summary>Tipp – Viele rote Fehler auf einmal?</summary>

Gehen Sie in der Reihenfolge 1 → 6 vor. Nach Schritt 1 sind alle Stellen rot, die
noch mit der Liste arbeiten – sie zeigen Ihnen genau, was Sie anpassen müssen.
</details>

**Denkfrage:** Was passiert, wenn Sie zweimal „Einkaufen“ eintragen? Warum?
(→ `docs/bonus.md`)
