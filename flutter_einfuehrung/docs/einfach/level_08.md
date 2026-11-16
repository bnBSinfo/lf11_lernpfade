# Level 8 – Abhaken: von der List zur Map

**Ziel:** Jedes ToDo hat jetzt 2 Werte: den Titel und den Haken. Darum wird aus der Liste eine `Map<String, bool>`.

**Du änderst:** `lib/todo_list.dart` und `lib/todo_item.dart` · **Skript:** Beispiel 2d

## Auftrag
Mach die Schritte in der Reihenfolge 1 bis 6. Nach Schritt 1 sind viele Stellen rot. Das ist normal. Genau diese Stellen änderst du danach.

1. **✏️ Ändern** `lib/todo_list.dart`. Ersetze die Liste durch eine Map.
   {{code 0}}
2. **✏️ Ändern** `lib/todo_list.dart`. `addItem` und `deleteItem` arbeiten jetzt mit der Map.
   {{code 1}}
3. **✏️ Ändern** `lib/todo_list.dart`. Füge die Methode `checkBoxDone` ein. Sie steht **unter** `deleteItem`.
   {{code 2}}
4. **✏️ Ändern** `lib/todo_item.dart`. Füge 2 Felder hinzu. Ersetze den Konstruktor.
   {{code 3}}
5. **✏️ Ändern** `lib/todo_item.dart`. Die Checkbox wird aktiv. Lösche das `const`.
   {{code 4}}
6. **✏️ Ändern** `lib/todo_list.dart`. Ersetze im `itemBuilder` die Zeile mit `return`.
   {{code 5}}

## Profi-Auftrag
- Jedes ToDo ist erledigt oder nicht. Die Checkbox zeigt das. Antippen schaltet um.
- Die Daten sind eine `Map<String, bool>`: Titel → erledigt.
- `ToDoItem(title, done, remove, checkBoxDone)` bleibt Stateless.
- Hinzufügen und Löschen gehen weiter.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Warum eine Map?** Jedes ToDo hat jetzt **2** Werte: Titel und Haken. Eine `List<String>` hat pro Platz nur 1 Wert. Eine `Map<String, bool>` hat Paare. Jeder **Schlüssel** (Titel) hat einen **Wert** (Haken ja oder nein).

{{code 6}}

| Aufgabe | List | Map |
|---|---|---|
| hinzufügen | `todos.add('Milch')` | `todos['Milch'] = false` |
| löschen | `todos.removeAt(i)` | `todos.remove('Milch')` |
| Anzahl | `todos.length` | `todos.length` |
| Eintrag Nr. i | `todos[i]` | Schlüssel: `todos.keys.elementAt(i)` · Wert: `todos.values.elementAt(i)` |

**Der Haken geht wie das Löschen:** Die Checkbox ist im `ToDoItem`. Die Daten sind im State der Liste.

1. Du tippst die Checkbox an. Dann läuft `checkBoxDone()`.
2. `checkBoxDone` ist die Funktion `() => checkBoxDone(key)` aus der Liste.
3. `todos.update(key, (bool done) => !done)` dreht den Wert um. Aus `false` wird `true`. Aus `true` wird `false`.
4. `setState` läuft. `build` läuft. Das `ToDoItem` bekommt den neuen Wert `done`. Es zeigt den Haken.

**Wichtig:** `ToDoItem` bleibt **Stateless**. Es merkt sich den Haken nicht. Es bekommt ihn jedes Mal neu von außen. So passen Anzeige und Daten immer zusammen.

<details><summary>Tipp – Viele rote Fehler auf einmal?</summary>

Geh der Reihe nach: 1 bis 6. Nach Schritt 1 sind alle Stellen rot, die noch die Liste nutzen. Sie zeigen dir, was du ändern musst.
</details>

**Denkfrage:** Du trägst 2-mal „Einkaufen“ ein. Was passiert? Warum?
