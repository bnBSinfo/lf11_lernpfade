# Level 5 – Ein Widget für ein Listenelement

**Ziel:** Du baust ein Stateless Widget für 1 ToDo. Du kannst es immer wieder benutzen.

**Du schreibst neu:** `lib/todo_item.dart` und `lib/todo_app.dart` · **Du änderst:** `lib/main.dart` · **Skript:** Beispiel 2a

## Planung (Skript)
Die fertige App braucht 4 Dinge: eine Liste von ToDos, eine Checkbox zum Abhaken, einen Button zum Löschen und einen Button zum Hinzufügen. Du fängst mit **1** Eintrag an.

## Auftrag
1. **📄 Neue Datei** `lib/todo_item.dart`. Darin steht das Stateless Widget `ToDoItem`. Tipp: `stless` + Tab. Den Titel bekommt es über den Konstruktor.
   {{code 0}}
   In `children` der `Row` kommen 3 Widgets:
   - `const Checkbox(value: false, onChanged: null)`. Sie ist noch grau.
   - `Expanded(child: Text(title))`
   - `const IconButton(icon: Icon(Icons.delete), onPressed: null)`. Er ist noch grau.
2. **📄 Neue Datei** `lib/todo_app.dart`. Darin steht das Stateless Widget `ToDoApp`. Es zeigt zur Probe 3 Einträge.
   {{code 1}}
3. **✏️ Ändern** `lib/main.dart`. Ersetze 2 Zeilen. Jetzt startet die `ToDoApp`.
   {{code 2}}
   Lösche `my_first_app.dart` und `my_login.dart` **nicht**. Du brauchst sie in Level 9 wieder.

## Profi-Auftrag
- `lib/todo_item.dart`: Stateless Widget `ToDoItem`. Der Titel kommt als 1. Wert in den Konstruktor.
  1 Zeile zeigt: Checkbox (grau) · Titel (nimmt den Platz) · Mülleimer-Button (grau).
- `lib/todo_app.dart`: `ToDoApp` zeigt 3 `ToDoItem`s in einer `ListView`. Eins heißt „Einkaufen“. Die AppBar heißt „ToDo-Element (Vorschau)“.
- `main.dart` startet `ToDoApp`. Die Login-Dateien bleiben.

*Kommst du nicht weiter? Schalte oben auf **🧭 Begleitet** um.*

## Erklärt – was passiert hier?

**Warum ist `ToDoItem` Stateless?** Ein Eintrag zeigt nur an. Er ändert nichts. Den Titel bekommt er von außen. Das geht über den Konstruktor:

{{code 3}}

So benutzt du 1 Widget für viele Titel. Wie eine Schablone.

**So ist die Zeile gebaut:**

- `Row` legt ihre Kinder **nebeneinander**. `Column` legt sie untereinander.
- `Checkbox(value: false, onChanged: null)`: `value` ist der Haken. `onChanged: null` macht sie grau. In Level 8 wird sie aktiv.
- `Expanded` nimmt den ganzen Rest-Platz. Darum steht der Mülleimer ganz rechts.
- `IconButton` ist ein Button mit Bild. `Icons.delete` ist der Mülleimer.

**`const` oder nicht?** `const Checkbox(...)` geht. Darin ändert sich nichts. `Text(title)` geht nicht mit `const`. Der Titel steht erst beim Start fest.

<details><summary>Tipp 1 – Wozu Expanded?</summary>

`Expanded` gibt dem Text den Rest-Platz. Dann steht der Mülleimer ganz rechts.
</details>

<details><summary>Tipp 2</summary>

{{code 4}}
</details>

> **Merke:** Ein Stateless Widget bekommt seine Daten von außen. Es ändert sie nie selbst. Dafür gibt es `final` und den `const`-Konstruktor.
