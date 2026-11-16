# Level 6 – Die ToDo-Liste

**Ziel:** Ein Stateful Widget hat eine Liste. Daraus baut es `ToDoItem`s. Neue Einträge kommen über einen Dialog.

**Du schreibst neu:** `lib/todo_list.dart` · **Du änderst:** `lib/todo_app.dart` · **Skript:** Beispiel 2b

## Auftrag
1. **📄 Neue Datei** `lib/todo_list.dart`. Darin steht das **Stateful Widget** `ToDoList`. Tipp: `stful` + Tab. So sieht der Rahmen aus:
   {{code 0}}
2. `addItem(String item)`: Schreibe `setState`. Darin: `todos.add(item)`. Danach, nach `setState`: `Navigator.of(context).pop();`. Das schließt den Dialog.
3. `newEntry()`: Rufe `showDialog` auf. Er zeigt einen `AlertDialog`. Sein `content` ist `TextField(onSubmitted: addItem)`.
4. Im `Scaffold` ersetzt du den Kommentar durch 3 Teile:
   - `appBar: AppBar(title: Text('ToDo Liste'))`
   - `body: ListView.builder(itemCount: todos.length, itemBuilder: …)`. Für jedes `i` baut er `ToDoItem(todos[i])`.
   - `floatingActionButton: FloatingActionButton(onPressed: newEntry, child: Icon(Icons.add))`
5. **✏️ Ändern** `lib/todo_app.dart`. Die Probe aus Level 5 brauchst du nicht mehr. Ersetze den Import. Ersetze den ganzen Inhalt von `build`.
   {{code 1}}

## Profi-Auftrag
- `lib/todo_list.dart`: Stateful Widget `ToDoList`. Die Titel liegen als Liste im State.
- Oben: AppBar „ToDo Liste“. Darunter: 1 `ToDoItem` pro Eintrag (`ListView.builder`). Unten rechts: ein Plus-Button.
- Plus öffnet einen `AlertDialog` mit Textfeld. Enter fügt den Eintrag hinzu. Dann geht der Dialog zu.
- `ToDoApp` startet gleich die `ToDoList`.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Warum ist `ToDoList` Stateful?** Die Liste ändert sich. Es kommen Einträge dazu. Darum braucht sie einen State. Im State steht `todos`.

**`ListView.builder` baut eine Liste aus Daten:**

{{code 2}}

Du schreibst nicht jedes `ToDoItem` selbst. Du sagst nur 2 Dinge: Wie viele gibt es? Wie baut man 1 Eintrag? Hat `todos` 2 Einträge? Dann ruft Flutter `itemBuilder` 2-mal auf: mit `i = 0` und `i = 1`.

**Der Dialog in 5 Schritten:**

1. Du tippst auf `+`. Dann läuft `newEntry()`.
2. `showDialog(...)` zeigt den `AlertDialog` über der Seite.
3. Du drückst Enter im Textfeld. Dann läuft `addItem('Milch kaufen')`.
4. `addItem` fügt den Text in `setState` zu `todos` hinzu. `build` läuft neu. Die Liste ist 1 länger.
5. `Navigator.of(context).pop()` schließt den Dialog. Ein Dialog ist wie eine kleine Seite. `pop` nimmt die oberste Seite weg.

**Stateful und Stateless arbeiten zusammen:** `ToDoList` hat die Daten. `ToDoItem` zeigt 1 Eintrag.

<details><summary>Tipp 1 – showDialog</summary>

{{code 3}}
</details>

<details><summary>Tipp 2 – ListView.builder</summary>

{{code 4}}
</details>

> **Merke:** `onPressed: newEntry` hat keine Klammern. So gibst du die Methode weiter. Mit Klammern läuft sie sofort.

**Achtung Skript:** Dort heißt die Liste 1-mal `products`. Schreibe überall `todos`.
